from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register('products', views.ProductView)
router.register('categories', views.CategoryView)
router.register('add', views.OrderItemViewSet)
router.register('orders', views.OrderViewSet)

app_name = 'ecommerce'

urlpatterns = [
    path('', include(router.urls)),
]