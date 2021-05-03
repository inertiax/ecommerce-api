from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register("comment", views.CommentViewSet)
router.register("category", views.CategoryViewSet)
router.register("product", views.ProductViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("cart/", views.CartAPIView.as_view()),
    path("cart/<product_id>/", views.CheckCartProduct.as_view()),
]
