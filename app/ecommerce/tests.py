import json

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from model_bakery import baker
from model_bakery.recipe import Recipe, seq, foreign_key

from . import serializers
from .models import Cart, Product, Category


class CategoryViewSetTest(APITestCase):

    endpoint = '/category/'

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="test123")
        self.client.force_authenticate(self.user)
        # refresh = RefreshToken.for_user(self.user)
        # self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    def test_category_get(self):
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_create(self):
        category = baker.make(Category)
        expected_json = {
            'title': category.title,
            'sub_category': category.sub_category
        }
        response = self.client.post(self.endpoint, data=expected_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_category_update(self):
        old_category = baker.make(Category)
        new_category = baker.make(Category)
        expected_json = {
            'title': new_category.title,
            'sub_category': new_category.sub_category
        }
        url = f'{self.endpoint}{old_category.id}/'
        response = self.client.put(
            url,
            data=expected_json,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_delete(self):
        category = baker.make(Category)
        url = f'{self.endpoint}{category.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ProductViewSetTest(APITestCase):

    endpoint = '/product/'

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@amine.com',
            'test123'
        )
        self.client.force_authenticate(self.user)
        # refresh = RefreshToken.for_user(self.user)
        # self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    def test_product_get(self):
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_create(self):
        product = baker.make(Product)
        expected_json = {
            'category': product.category
        }
        # payload = serializers.ProductSerializer(product).data
        response = self.client.post(self.endpoint, data=expected_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


# class CheckoutViewTestCase(APITestCase):
#
#     def setUp(self):
#         self.client = APIClient()
#         self.user = get_user_model().objects.create_user(
#             'test@amine.com',
#             'test123'
#         )
#         self.client.force_authenticate(self.user)
#         self.cart = baker.make('Cart')
#         # refresh = RefreshToken.for_user(self.user)
#         # self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
#
#     def test_get_checkout(self):
#         sample_order(cart=self.cart)
#         print(self.cart)
#         response = self.client.get("/checkout/")
#         print(response)
#
#         orders = Order.objects.all().order_by('-id')
#         serializer = DetailedOrderSerializer(orders, many=True)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data, serializer.data)
