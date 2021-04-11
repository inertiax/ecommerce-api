from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


class TransactionViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    # def test_category_failure(self):

