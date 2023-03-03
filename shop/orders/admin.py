from django.contrib import admin

from orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('initiator', 'quantity', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__email', 'product__name')
    readonly_fields = ('id', 'created_at')
