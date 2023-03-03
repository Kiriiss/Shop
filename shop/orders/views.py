from http import HTTPStatus
import stripe
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, TemplateView, DetailView
from django.views.generic.list import ListView
from common.Mixins import TitleMixin
from orders.forms import OrderForm
from products.models import Product, Cart
from shop import settings
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from orders.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Store - Спасибо за заказ'


class СancledTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/cancled.html'
    title = 'Store - Заказ отменен'


class OrderListview(TitleMixin, ListView):
    template_name = 'orders/orders.html'
    title = 'Store - Заказы'
    queryset = Order.objects.all()
    ordering = ('-id')

    def get_queryset(self):
        queryset = super(OrderListview, self).get_queryset()
        return queryset.filter(initiator=self.request.user)


class OrderDetailView(DetailView):
    template_name = 'orders/order-detail.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['title'] = f'Store - Заказ #{self.object.id}'
        return context


class OrderCreateView(TitleMixin, CreateView):
    title = 'Shop - order create'
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        baskets = Cart.objects.filter(user=self.request.user)
        checkout_session = stripe.checkout.Session.create(
            line_items=baskets.stripe_products(),
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_canceled')),

        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
        session = stripe.checkout.Session.retrieve(
            event['data']['object']['id'],
            expand=['line_items'],
        )

        line_items = session.line_items
        # Fulfill the purchase...
        fulfill_order(line_items)

    # Passed signature verification
    return HttpResponse(status=200)


def fulfill_order(line_items):
    order_id = int(line_items.metadata.order_id)
    order = Order.objects.get(id=order_id)
    order.update_after_payment()
