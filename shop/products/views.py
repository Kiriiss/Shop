from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from products.models import Product, Category, Cart


def about(request):
    return render(request, 'products/about.html')


def contact(request):
    return render(request, 'products/contact.html')


def home_view(request, ):
    products = Product.objects.filter(is_featured=True)[:3]
    context = {'products': products, }
    return render(request, 'products/index.html', context)


def product_list(request, id=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(is_featured=True)
    if id:
        category = get_object_or_404(Category, id=id)
        products = products.filter(category=category)
    paginator = Paginator(products, 2)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    context = {
        'category': category,
        'categories': categories,
        'products': products,
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'products/product_detail.html', {'product': product})


def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Cart.objects.get_or_create(user=request.user, product=product)
    if not baskets.exists():
        Cart.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
