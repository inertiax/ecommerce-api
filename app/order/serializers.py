from rest_framework import serializers

from .models import Order
from ecommerce.models import Product


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    product_name = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Product.objects.all()
    )
    class Meta:
        model = Order
        fields = ['id', 'user', 'product_name', 'total_product']
        read_only_fields = ('id',)
