from rest_framework import serializers

from ecommerce.serializers import CartSerializer
from order.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "order_id",
            "create_date",
            "shipping",
            "cart_total",
            "tax_total",
            "total",
        ]


class DetailedOrderSerializer(serializers.ModelSerializer):
    cart = CartSerializer()

    class Meta:
        model = Order
        fields = [
            "order_id",
            "cart",
            "create_date",
            "cart_total",
            "tax_total",
            "shipping",
            "total",
        ]
