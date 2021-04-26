from rest_framework import serializers
from rest_framework.fields import Field

from ecommerce.serializers import CartSerializer, ProductSerializer
from order.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        get_cart_total = Field(source="get_cart_total")
        get_tax_total = Field(source="get_tax_total")
        get_total = Field(source="get_total")
        fields = [
            "order_id",
            "create_date",
            "shipping",
            "get_cart_total",
            "get_tax_total",
            "get_total",
        ]


class DetailedOrderSerializer(serializers.ModelSerializer):
    cart = CartSerializer()

    class Meta:
        model = Order
        get_cart_total = Field(source="get_cart_total")
        get_tax_total = Field(source="get_tax_total")
        get_total = Field(source="get_total")
        fields = [
            "order_id",
            "cart",
            "create_date",
            "get_cart_total",
            "get_tax_total",
            "shipping",
            "get_total",
        ]
