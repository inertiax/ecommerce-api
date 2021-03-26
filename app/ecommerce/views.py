from rest_framework import viewsets, mixins, generics
from rest_framework.authtoken import views
from rest_framework.settings import api_settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from django.contrib.auth.models import User

from . import models
from . import serializers


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all().order_by('name')
    
    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class CategoryView(viewsets.ModelViewSet):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all().order_by('id')
    
    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class ProductView(viewsets.ModelViewSet):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    # def get_queryset(self):
    #     return self.queryset.filter(user=self.request.user).order_by('-id')


class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.OrderItemSerializer
    queryset = models.OrderItem.objects.all()
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    # def get_queryset(self):
    #     return self.queryset.filter(product__order=self.request.date_added).order_by('-id')

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.OrderSerializer
    queryset = models.Order.objects.all()
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    # def get_queryset(self):
    #     return self.queryset.filter(user=self.request.user).order_by('-id')