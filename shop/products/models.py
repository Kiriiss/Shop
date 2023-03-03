import stripe
from django.db import models
from shop import settings
from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY


class Category(models.Model):
    objects = None
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    objects = None
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='products', blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_featured = models.BooleanField(default=False)
    stripe_product_price_id = models.CharField(max_length=128, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price['id']
        super(Product, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'], unit_amount=round(self.price * 100), currency='USD')
        return stripe_product_price


class BasketQueryset(models.QuerySet):

    def total_cart_price(self):
        return sum(item.total_item_price() for item in self)

    def total_quantity(self):
        return sum(item.quantity for item in self)

    def stripe_products(self):
        line_items = []
        for basket in self:
            item = {
                'price': basket.product.stripe_product_price_id,
                'quantity': basket.quantity,
            }
            line_items.append(item)
        return line_items


class Cart(models.Model):
    objects = BasketQueryset.as_manager()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='carts')
    quantity = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Корзина для {self.user.email} | продукт:{self.product.name}'

    def total_item_price(self):
        return self.quantity * self.product.price

    def de_json(self):
        basket_item = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.total_item_price())
        }
        return basket_item
