from rest_framework import routers
from django.urls import path, include

from . import views


router = routers.DefaultRouter()
router.register('', views.UserViewSet)
# user_list = views.UserViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })

app_name = 'user'

urlpatterns = [
    # path('', user_list, name='user-list'),
    path('', include(router.urls)),
    path('logout/', views.Logout.as_view()),
    path('token/', views.CreateTokenView.as_view(), name='token'),
]
