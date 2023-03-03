from django.contrib import admin

from products.models import Category,Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'image', 'price', 'is_featured', 'category','stripe_product_price_id')
    list_filter = ('category', 'is_featured')