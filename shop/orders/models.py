from django.db import models
from users.models import User
from django.conf import settings
from products.models import Product, Cart


class Order(models.Model):
    objects = None
    CREATED = 1
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    CANCELED = 4
    STATUSES = (
        (CREATED, 'Created'),
        (PAID, 'Paid'),
        (ON_WAY, 'On way'),
        (DELIVERED, 'Delivered'),
        (CANCELED, 'Canceled'),
    )
    initiator = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    total_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    address = models.CharField(max_length=250, default='')
    basket_history = models.JSONField(default=dict)
    status = models.CharField(max_length=20, choices=STATUSES, default=CREATED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.initiator.email} | {self.status}'

    def update_after_payment(self):
        baskets = Cart.objects.filter(user=self.initiator)
        self.status = self.PAID
        self.basket_history = {
            'purchased_items': [basket.de_json() for basket in baskets],
            'total_cart_price': float(baskets.total_cart_price()),
        }
        baskets.delete()
        self.save()
