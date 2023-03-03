from django.urls import path
from products.views import  about, home_view, contact, product_list, product_detail, add_to_cart

app_name= 'products'

urlpatterns = [
    path('', home_view, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('product_list', product_list, name='product_list'),
    path('product_detail/<int:id>/', product_detail, name='product_detail'),
    path('product_list_by_category<int:id>/', product_list, name='product_list_by_category'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),

]