from rest_framework import viewsets, status
from rest_framework.authtoken import views
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
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


class CartAPIView(views.APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CartSerializer
    
    def get(self, request, *args, **kwargs):
        cart_obj, _ = models.Cart.objects.get_existing_or_new(request)
        context = {'request': request}
        serializer = self.serializer_class(cart_obj, context=context)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        product_id = request.data.get("id")
        quantity = int(request.data.get("quantity", 1))

        product_obj = get_object_or_404(models.Product, pk=product_id)
        cart_obj, _ = models.Cart.objects.get_existing_or_new(request)

        if quantity <= 0:
            cart_item_qs = models.CartItem.objects.filter(
                cart=cart_obj, product=product_obj)
            if cart_item_qs.count != 0:
                cart_item_qs.first().delete()
        else:
            cart_item_obj, created = models.CartItem.objects.get_or_create(
                product=product_obj, cart=cart_obj)
            cart_item_obj.quantity = quantity
            cart_item_obj.save()

        serializer = serializers.CartSerializer(cart_obj, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CheckCartProduct(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, *args, product_id, **kwargs):
        product_obj = get_object_or_404(models.CartItem, pk=product_id)
        product_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, *args, product_id, **kwargs):
        product_obj = get_object_or_404(models.Product, pk=product_id)
        cart_obj, created = models.Cart.objects.get_existing_or_new(request)
        serializer = serializers.CartItemSerializer(cart_obj, {'request': request})
        # return Response(not created and models.CartItem.objects.filter(cart=cart_obj, product=product_obj).exists())
        return Response(serializer.data, status=status.HTTP_200_OK)
        

# class ProductView(viewsets.ModelViewSet):
#     serializer_class = serializers.ProductSerializer
#     queryset = models.Product.objects.all()
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    # def get_queryset(self):
    #     return self.queryset.filter(user=self.request.user).order_by('-id')


# class OrderItemViewSet(viewsets.ModelViewSet):
#     serializer_class = serializers.OrderItemSerializer
#     queryset = models.OrderItem.objects.all()
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    # def get_queryset(self):
    #     return self.queryset.filter(product__order=self.request.date_added).order_by('-id')

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


# class OrderViewSet(viewsets.ModelViewSet):
#     serializer_class = serializers.OrderSerializer
#     queryset = models.Order.objects.all()
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    # def get_queryset(self):
    #     return self.queryset.filter(user=self.request.user).order_by('-id')