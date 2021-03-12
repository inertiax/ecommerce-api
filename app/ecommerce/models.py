from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User


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
    SHOE_SIZES = (
        (37, 37),
        (39, 39),
        (41, 41),
        (43, 43),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    shirt_size = models.TextField(max_length=2, choices=SHIRT_SIZES, default='M')
    shoe_size = models.IntegerField(choices=SHOE_SIZES, default=37)
    color = models.TextField(max_length=10, choices=COLORS, default='BLACK')
    # image = models.ImageField(default='default.jpg', upload_to='product_pics')
    price = models.FloatField()
    stock = models.IntegerField()
    description = models.TextField(max_length=1000, null=False, blank=True)
    create_date = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
