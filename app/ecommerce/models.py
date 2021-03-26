from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings

from app.settings import MEDIA_URL


SHIRT_SIZES = (
    ('XS', 'XS'),
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
)
COLORS = (
    ('WHITE', 'white'),
    ('BLACK', 'black'),
    ('BLUE', 'blue'),
    ('GREEN', 'green'),
)


class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def get_products(self):
        return self.get_queryset().filter(active=True)


class Category(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Product(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    size = models.TextField(max_length=2, choices=SHIRT_SIZES, null=True, blank=True)
    color = models.TextField(max_length=10, choices=COLORS, null=True, blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=4, decimal_places=2, default=18)
    
    stock = models.IntegerField()
    description = models.TextField(max_length=1000, null=False, blank=True)
    active = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    objects = ProductManager()

    def __str__(self):
        return self.name

    def get_image_url(self):
        return f'{MEDIA_URL}{self.image}'


class Order(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
