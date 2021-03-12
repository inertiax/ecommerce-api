from rest_framework import serializers
from .models import Product, Category


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    create_date = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    last_modified = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    
    class Meta:
        model = Product
        fields = '__all__'
