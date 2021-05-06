from django.db import models
from django.contrib.auth import get_user_model
from django.core.files import File

from io import BytesIO
from PIL import Image

from app.settings import MEDIA_URL

User = get_user_model()


SHIRT_SIZES = (
    ("XS", "XS"),
    ("S", "S"),
    ("M", "M"),
    ("L", "L"),
    ("XL", "XL"),
)
COLORS = (
    ("WHITE", "white"),
    ("BLACK", "black"),
    ("BLUE", "blue"),
    ("GREEN", "green"),
)


class Category(models.Model):
    title = models.CharField(max_length=255)
    sub_category = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="sub_categories",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title


class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def get_products(self):
        return self.get_queryset().filter(active=True)


class Product(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE
    )
    size = models.TextField(max_length=2, choices=SHIRT_SIZES, null=True, blank=True)
    color = models.TextField(max_length=10, choices=COLORS, null=True, blank=True)
    image = models.FileField()  # models.ImageField(upload_to="images/", blank=True, null=True)

    original_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
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


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="comments"
    )
    reply = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True, related_name="replies"
    )
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    def children(self):
        return Comment.objects.filter(reply=self)

    @property
    def is_reply(self):
        if self.reply is not None:
            return False
        return True

    @property
    def get_reply_count(self):
        if self.is_reply:
            return self.children().count()
        return 0


class CartManager(models.Manager):
    def get_existing_or_new(self, request):
        created = False
        cart_id = request.session.get("cart_id")

        if self.get_queryset().filter(id=cart_id, used=False).count() == 1:
            obj = self.model.objects.get(id=cart_id)
        elif self.get_queryset().filter(user=request.user, used=False).count() == 1:
            obj = self.model.objects.get(user=request.user, used=False)
            request.session["cart_id"] = obj.id
        else:
            obj = self.model.objects.create(user=request.user)
            request.session["cart_id"] = obj.id
            created = True
        return obj, created


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    used = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)

    @property
    def get_total(self):
        total = 0
        for item in self.products.all():
            total += item.product.price * item.quantity
        return total

    @property
    def get_tax_total(self):
        total = 0
        for item in self.products.all():
            total += item.product.price * item.quantity * item.product.tax / 100
        return total

    @property
    def get_cart_total(self):
        return sum(item.quantity for item in self.products.all())


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="products")

    class Meta:
        unique_together = ("product", "cart")
