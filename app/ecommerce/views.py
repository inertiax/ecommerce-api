from rest_framework import viewsets, mixins, generics
from rest_framework.authtoken import views
from rest_framework.settings import api_settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer, \
                            UserSerializer, AuthTokenSerializer


# class RegistrationView(views.ObtainAuthToken):
#     serializer_class = RegistrationSerializer
#     renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class CreateUserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class CreateTokenView(views.ObtainAuthToken):
    """create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ProductView(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
