from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class RegistrationTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def test_registration(self):
        data = {"email": "test123@test.com",
                "password": "12345",
                "name": "testname",
                "surname": "testsurname"}
        response = self.client.post("/user/signup/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(data['password']))
        self.assertNotIn('password', response.data)

    def test_user_exists(self):
        """test creating user that already created fails"""
        payload = {'email': 'test@amine.com',
                   'password': 'test123',
                   'name': 'test'}
        create_user(**payload)

        res = self.client.post("/user/signup/", payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """test that password should be more than 5 char"""
        payload = {'email': 'test@amine.com',
                   'password': 'test',
                   'name': 'Test'}
        res = self.client.post("/user/signup/", payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)


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
