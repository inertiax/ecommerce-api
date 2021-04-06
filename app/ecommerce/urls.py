from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('comment', views.CommentViewSet)
router.register('category', views.CategoryViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('product/list/', views.ProductView.as_view()),  # {'get': 'list'}
    # path('product/list/<id>/', views.ProductView.as_view()),  # {'get': 'retrieve'}
    # path('category/list/', views.CategoryView.as_view()),  # {'get': 'list'}
    # path('category/list/<id>/', views.CategoryView.as_view({'get': 'retrieve'})),
    path('cart/', views.CartAPIView.as_view()),
    path('cart/<product_id>/', views.CheckCartProduct.as_view()),
]
