from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register('products', views.ProductView)
router.register('categories', views.CategoryView)
router.register('users', views.CreateUserView)

urlpatterns = [
    path('', include(router.urls)),
    path('register', views.CreateTokenView.as_view(), name='register'),
]