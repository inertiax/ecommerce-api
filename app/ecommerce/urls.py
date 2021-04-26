from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register("comment", views.CommentViewSet, basename='comment')
router.register("category", views.CategoryViewSet, basename='category')
router.register("product", views.ProductViewSet, basename='product')


urlpatterns = [
    path("", include(router.urls)),
    path("cart/", views.CartAPIView.as_view()),
    path("cart/<product_id>/", views.CheckCartProduct.as_view()),
]
