from rest_framework import serializers, fields
from rest_framework.fields import Field

from .models import Product, Category, Cart, CartItem, Comment
from user.serializers import UserSerializer


class ChildCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title"]


class CategoryWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title", "sub_category"]


class CategoryReadSerializer(serializers.ModelSerializer):
    sub_category = ChildCategorySerializer(read_only=True)

    class Meta:
        model = Category
        fields = ["id", "title", "sub_category"]


class ProductSerializer(serializers.ModelSerializer):
    # category = CategoryWriteSerializer(read_only=True)
    image = fields.FileField(max_length=None, use_url=True, allow_null=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "brand",
            "category",
            "size",
            "color",
            "original_price",
            "price",
            "stock",
            "description",
            "image",
            "create_date",
            "last_modified",
        ]

    # def create(self, validated_data):
    #     validated_data["category"] = Category.objects.create(
    #         **validated_data.get("category", {})
    #     )
    #     product = Product.objects.create(**validated_data)
    #     return product


class ChildCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "user", "content", "create_date"]


class CommentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        get_reply_count = Field(source="get_reply_count")
        fields = [
            "id",
            "user",
            "product",
            "content",
            "reply",
            "get_reply_count",
            "create_date",
        ]


class CommentReadSerializer(serializers.ModelSerializer):
    reply = ChildCommentSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        get_reply_count = Field(source="get_reply_count")
        fields = [
            "id",
            "user",
            "product",
            "content",
            "reply",
            "get_reply_count",
            "create_date",
        ]


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity"]


class CartSerializer(serializers.ModelSerializer):
    products = CartItemSerializer(read_only=True, many=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Cart
        get_total = Field(source="get_total")
        get_tax_total = Field(source="get_tax_total")
        get_cart_total = Field(source="get_cart_total")
        fields = [
            "id",
            "user",
            "products",
            "get_total",
            "get_tax_total",
            "get_cart_total",
        ]
