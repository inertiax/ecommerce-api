from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from .models import Product, Category, Order, OrderItem
from user.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']
        read_only_fields = ('id',)


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    
    # image = serializers.ImageField(max_length=None, allow_empty_file=False,
    #                                allow_null=True, required=False)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'brand', 'category', 'size', 'color', 'original_price',
                  'price', 'stock', 'description', 'image', 'create_date', 'last_modified']


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Product.objects.all()
    )
    order = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Order.objects.all()
    )
    date_added = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['product', 'order', 'quantity', 'date_added']
        read_only_fields = ('id',)
    
    def get_date_added(self, obj):
        return obj.date_added.strftime("%m/%d/%Y, %H:%M:%S")


class OrderSerializer(serializers.ModelSerializer):
    # user = serializers.SerializerMethodField(read_only=True)
    order = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('id',)

    def get_order(self, obj):
        orderitems = obj.orderitem_set.all()
        serializer = OrderItemSerializer(orderitems, many=True)
        return serializer.data
    
    # def get_user(self,obj):
    #     user = obj.user
    #     serializer = UserSerializer(user, many=False)
    #     return serializer.data
