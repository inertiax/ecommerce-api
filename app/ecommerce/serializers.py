from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, Category


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']
        read_only_fields = ('id',)


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all()
    )
    user = serializers.ReadOnlyField(source='user.username')
    image = serializers.ImageField(max_length=None, allow_empty_file=False,
                                   allow_null=True, required=False)
    
    class Meta:
        model = Product
        fields = ['id', 'user', 'name', 'brand', 'category', 'size', 'color', 'price',
                  'stock', 'description', 'image', 'create_date', 'last_modified']
        read_only_fields = ('id',)
