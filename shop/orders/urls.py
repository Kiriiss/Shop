from django.urls import path

from orders.views import OrderCreateView, SuccessTemplateView, СancledTemplateView, OrderListview, OrderDetailView

app_name = 'orders'

urlpatterns = [
    path('order_create/', OrderCreateView.as_view(), name='order_create'),
    path('order_success/', SuccessTemplateView.as_view(), name='order_success'),
    path('order_canceled/', СancledTemplateView.as_view(), name='order_canceled'),
    path('orders/', OrderListview.as_view(), name='orders'),
    path('detail_order/<int:pk>/', OrderDetailView.as_view(), name='order_detail')

]
