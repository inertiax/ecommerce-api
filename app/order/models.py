from django.db import models

from ecommerce.models import Cart


class OrderManager(models.Manager):
    
    def get_queryset(self):
        return super().get_queryset().filter()

    def get_order(self, cart):
        return self.get_queryset().filter(cart=cart)


class Order(models.Model):
    order_id = models.CharField(max_length=100, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    shipping = models.DecimalField(default=10, max_digits=10, decimal_places=2)
    
    objects = OrderManager()
    
    def __str__(self):
        return self.order_id
    
    @property
    def cart_total(self):
        return self.cart.get_total
    
    @property
    def tax_total(self):
        return self.cart.get_tax_total
    
    @property
    def total(self):
        return self.cart_total + self.tax_total + self.shipping
    
    # def check_done(self):
    #     total = self.total
    #     cart = self.cart
    #     active = self.active
    #     if active and total > 0 and cart:
    #         return True
    #     return False
    

# class Order(models.Model):
#     create_date = models.DateTimeField(auto_now_add=True)
#     update_date = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return str(self.id)

#     @property
#     def get_cart_total(self):
#         orderitems = self.orderitem_set.all()
#         total = sum([item.get_total for item in orderitems])
#         return total

#     @property
#     def get_cart_items(self):
#         orderitems = self.orderitem_set.all()
#         total = sum([item.quantity for item in orderitems])
#         return total


# class OrderItem(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
#     order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
#     quantity = models.IntegerField(default=0, null=True, blank=True)
#     date_added = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return str(self.product)

#     @property
#     def get_total(self):
#         total = self.product.price * self.quantity
#         return total