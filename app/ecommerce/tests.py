from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from model_bakery import baker

import io
from PIL import Image

from . import serializers
from .models import Cart, Product, Category, CartItem


class CategoryViewSetTest(APITestCase):
    endpoint = '/category/'

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="test123")
        self.user.save()
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
        # self.client.force_authenticate(self.user)
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    def test_product_get(self):
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_create(self):
        product = baker.make(Product, _create_files=False)
        payload = serializers.ProductSerializer(product).data
        # print(payload)
        response = self.client.post(self.endpoint, data=payload, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_product_notcreate(self):
        product = baker.make(Product,
                             _create_files=False,
                             name='')
        payload = serializers.ProductSerializer(product).data
        # print(payload)
        response = self.client.post(self.endpoint, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CartViewTestCase(APITestCase):
    endpoint = '/cart/'

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@amine.com',
            'test123'
        )
        self.product = baker.make(Product)
        self.cart = baker.make(Cart, cart__products__id=1)
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    def test_cart_get(self):
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cart_post(self):
        payload = {
            'product_id': 1,
            'quantity': 5
        }
        response = self.client.post(self.endpoint, data=payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CheckCartProductTest(APITestCase):

    endpoint = '/cart/'

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@amine.com',
            'test123'
        )
        self.product = baker.make(Product)
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    def test_cart_item_delete(self):
        cart = baker.make(CartItem)
        url = f'{self.endpoint}{cart.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

# class ImageUploadTest(APITestCase):
#
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(
#             'test@amine.com',
#             'test123'
#         )
#         self.user.save()
#         refresh = RefreshToken.for_user(self.user)
#         self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
#
#     def generate_photo_file(self):
#         file = io.BytesIO()
#         image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
#         image.save(file, 'png')
#         file.name = 'test.png'
#         file.seek(0)
#         return file
#
#     def test_upload_image(self):
#         photo_file = self.generate_photo_file()
#         payload = {
#             'photo': photo_file
#         }
#         url = '/media/' + photo_file.name + '/'
#         print(url)
#         print(payload)
#         response = self.client.post(url, data=payload, format='multipart')
#         # print(response.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_cart_item_get(self):
    #     # print(self.product.__dict__)
    #     cart_item = baker.make(CartItem, cart__products__id=1)
    #     print(cart_item.__dict__)
    #     print(cart_item.product_id)
    #     url = f'{self.endpoint}{cart_item.product_id}/'
    #     print(url)
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
