import json

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from model_bakery import baker

from .serializers import DetailedOrderSerializer
from .models import Order
from ecommerce.models import Cart


def sample_order(cart, **params):
    defaults = {
        'active': True,
        'shipping': 10
    }
    defaults.update(params)

    return Order.objects.create(cart=cart, **defaults)


class CheckoutViewTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@amine.com',
            'test123'
        )
        self.client.force_authenticate(self.user)
        self.cart = baker.make('Order')
        # refresh = RefreshToken.for_user(self.user)
        # self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    def test_get_checkout(self):
        sample_order(cart=self.cart)
        print(self.cart)
        response = self.client.get("/checkout/")
        print(response)

        orders = Order.objects.all().order_by('-id')
        serializer = DetailedOrderSerializer(orders, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
