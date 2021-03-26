from django.urls import path, include

from . import views


urlpatterns = [
    path('list/', views.ProductViewSet.as_view({'get': 'list'})),
    path('list/<id>/', views.ProductViewSet.as_view({'get': 'retvieve'})),
]