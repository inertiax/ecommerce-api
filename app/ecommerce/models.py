from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings


class Category(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Product(models.Model):
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
    # SHOE_SIZES = ((i, i) for i in range(36, 46))

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    size = models.TextField(max_length=2, choices=SHIRT_SIZES, null=True, blank=True)
    # shoe_size = models.IntegerField(choices=SHOE_SIZES, default=37)
    color = models.TextField(max_length=10, choices=COLORS, null=True, blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    price = models.FloatField()
    stock = models.IntegerField()
    description = models.TextField(max_length=1000, null=False, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
