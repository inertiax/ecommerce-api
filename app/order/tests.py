from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from model_bakery import baker

from .serializers import DetailedOrderSerializer, OrderSerializer
from .models import Order
from ecommerce.models import Cart


class CheckoutViewTestCase(APITestCase):

    endpoint = '/checkout/'

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@amine.com',
            'test123'
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        self.cart = baker.make(Cart, cart__products__id=1)
        # print(self.cart.__dict__)
        self.order = baker.make(Order, cart=self.cart)
        print(self.order.__dict__)

    def test_order_get(self):
        response = self.client.get(self.endpoint)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_order_post(self):
        order = baker.make(Order,
                           cart__products__id=1,
                           cart__user=self.user)
        payload = DetailedOrderSerializer(order).data
        print(payload)
        response = self.client.post(self.endpoint, data=payload, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
