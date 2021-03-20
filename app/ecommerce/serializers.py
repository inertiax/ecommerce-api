from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, Category


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username', read_only=False)
    image = serializers.ImageField(max_length=None, allow_empty_file=False,
                                   allow_null=True, required=False)
    
    class Meta:
        model = Product
        fields = ['id', 'user', 'name', 'brand', 'category', 'size', 'color', 'price',
                  'stock', 'description', 'create_date', 'last_modified']
