from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register('products', views.ProductView)
router.register('categories', views.CategoryView)

urlpatterns = [
    path('', include(router.urls)),
]