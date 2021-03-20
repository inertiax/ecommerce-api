from django.db import models
from django.conf import settings

from ecommerce.models import Product


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, 
        blank=True)
    product_name = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE)
    total_product = models.CharField(max_length=500, default=0)
    total_amount = models.CharField(max_length=50, default=0)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
