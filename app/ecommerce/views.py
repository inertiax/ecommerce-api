from rest_framework import viewsets, mixins, generics
from rest_framework.authtoken import views
from rest_framework.settings import api_settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


class ProductView(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by('id')
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('title')
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
