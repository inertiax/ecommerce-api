from rest_framework import viewsets, status, generics
from rest_framework.authtoken import views
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.db.transaction import atomic

from . import models
from . import serializers


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all().order_by("id")
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ["GET"]:
            return serializers.CategoryReadSerializer
        return serializers.CategoryWriteSerializer

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


@method_decorator(atomic, name="dispatch")
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all().order_by("name")

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = models.Comment.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ["GET"]:
            return serializers.CommentReadSerializer
        return serializers.CommentWriteSerializer


class CartAPIView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        cart_obj, _ = models.Cart.objects.get_existing_or_new(request)
        context = {"request": request}
        serializer = serializers.CartSerializer(cart_obj, context=context)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        # Request Data
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        # Get Product Obj and Cart Obj
        product_obj = get_object_or_404(models.Product, pk=product_id)
        cart_obj, _ = models.Cart.objects.get_existing_or_new(request)

        if quantity <= 0:
            cart_item_qs = models.CartItem.objects.filter(
                cart=cart_obj, product=product_obj
            )
            if cart_item_qs.count != 0:
                cart_item_qs.first().delete()
        else:
            cart_item_obj, created = models.CartItem.objects.get_or_create(
                product=product_obj, cart=cart_obj
            )
            cart_item_obj.quantity = quantity
            cart_item_obj.save()
            # serializer = serializers.CartSerializer(cart_item_obj, context={'request': request})
            # return Response(serializer.data)

        serializer = serializers.CartSerializer(cart_obj, context={"request": request})
        return Response(serializer.data)


class CheckCartProduct(views.APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, product_id, **kwargs):
        product_obj = get_object_or_404(models.CartItem, pk=product_id)
        product_obj.delete()
        return Response("Product Deleted", status=status.HTTP_204_NO_CONTENT)

    def get(self, request, *args, product_id, **kwargs):
        product_obj = get_object_or_404(models.Product, pk=product_id)
        cart_obj, created = models.Cart.objects.get_existing_or_new(request)
        serializer = serializers.CartItemSerializer(cart_obj, {"request": request})
        # return Response(not created and models.CartItem.objects.filter(cart=cart_obj, product=product_obj).exists())
        return Response(serializer.data, status=status.HTTP_200_OK)
