import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer
from .models import User


class RegistrationTestCase(APITestCase):

    def test_registration(self):
        data = {"email": "test123", "password": "12345",
                "name": "testname", "surname": "testsurname"}
        response = self.client.post("/user/signup/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class GetUserViewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="test@test.com",
                                             password="test123")
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    def test_profile_list_authenticated(self):
        response = self.client.get("/user/get_user/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_list_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get("/user/get_user/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
