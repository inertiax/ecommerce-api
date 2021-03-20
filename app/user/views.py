from rest_framework import viewsets, generics, views, \
                            authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.response import Response

from user.serializers import UserSerializer, AuthTokenSerializer
from user.models import CustomUser


class CreateTokenView(ObtainAuthToken):
    """create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(ownew=self.request.user)

"""
login logout oluştur APIview ile
https://stackoverflow.com/questions/30739352/django-rest-framework-token-authentication-logout
"""
class Logout(views.APIView):

    def get(self, request, format=None):
        # delete the token to force logout
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
    
