from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Order
from .serializers import DetailedOrderSerializer
from ecommerce.models import Cart


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        cart = Order.objects.all()
        cart_obj, _ = Cart.objects.get_existing_or_new(request)
        if cart_obj.get_cart_total == 0:
            return Response({"error": "cart is empty"}, status=400)

        serializer = DetailedOrderSerializer(cart, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        cart_obj, _ = Cart.objects.get_existing_or_new(request)
        order_obj = Order.objects.get_order(cart_obj)
        return Response(DetailedOrderSerializer(order_obj).data)
