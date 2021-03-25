from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from .models import Product, Category, Order, OrderItem
from user.serializers import UserSerializer


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']
        read_only_fields = ('id',)


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='category-detail',
        queryset=Category.objects.all()
    )
    user = serializers.SerializerMethodField(read_only=True)
    image = serializers.ImageField(max_length=None, allow_empty_file=False,
                                   allow_null=True, required=False)
    
    class Meta:
        model = Product
        fields = ['id', 'user', 'name', 'brand', 'category', 'size', 'color', 'price',
                  'stock', 'description', 'image', 'create_date', 'last_modified']
        read_only_fields = ('id',)

    def get_user(self,obj):
        user = obj.user
        serializer = UserSerializer(user, many=False)
        return serializer.data


class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    product = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='product-detail',
        queryset=Product.objects.all()
    )
    order = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='order-detail',
        queryset=Order.objects.all()
    )

    class Meta:
        model = OrderItem
        fields = '__all__'
        read_only_fields = ('id',)


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    order = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('id',)

    def get_orderItems(self, obj):
        items = obj.orderitem_set.all()
        serializer = OrderItemSerializer(items, many=True)
        return serializer.data
    
    def get_user(self,obj):
        user = obj.user
        serializer = UserSerializer(user, many=False)
        return serializer.data
