from django.urls import path, include

from . import views


urlpatterns = [
    path('product/list/', views.ProductViewSet.as_view({'get': 'list'})),
    path('product/list/<id>/', views.ProductViewSet.as_view({'get': 'retvieve'})),
    path('cart/', views.CartAPIView.as_view()),
    path('cart/<product_id>/', views.CheckCartProduct.as_view()),
]