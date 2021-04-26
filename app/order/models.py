from django.db import models
from django.contrib.auth import settings
from django.contrib.auth import get_user_model
from ecommerce.models import Cart, Product


User = get_user_model()


class OrderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter()

    def get_order(self, cart):
        qs = self.get_queryset().filter(cart__user=cart.user)
        if qs.count() == 0:
            cart = cart.user.cart_set.filter(used=False).first()
            order = Order(cart=cart)
            order.save()
            return order
        else:
            order = qs.first()
            order.save()
            return order


class Order(models.Model):
    order_id = models.CharField(max_length=100, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='carts')
    active = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    shipping = models.DecimalField(default=10, max_digits=10, decimal_places=2)

    objects = OrderManager()

    def __str__(self):
        return self.order_id

    @property
    def get_cart_total(self):
        return self.cart.get_total

    @property
    def get_tax_total(self):
        return self.cart.get_tax_total

    @property
    def get_total(self):
        return self.cart_total + self.tax_total + self.shipping
