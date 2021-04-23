from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics

from .serializers import UserSerializer

User = get_user_model()


# class RegisterView(generics.CreateAPIView):
#     serializer_class = UserSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        name = request.data.get("name")
        surname = request.data.get("surname")
        user = User.objects.create_user(
            email=email, password=password, name=name, surname=surname
        )
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

        # email = request.data.get("email")
        # password = request.data.get("password")
        # name = request.data.get("name")
        # surname = request.data.get("surname")
        # try:
        #     user = User.objects.create_user(
        #         email=email, password=password, name=name, surname=surname)
        #     return Response(UserSerializer(user).data)
        # except ValueError as err:
        #     return Response({'error': "Provide Invalid Details"}, status=400)
        # except IntegrityError as err:
        #     return Response({'error': "User Already Exist"}, status=403)


class GetUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response(UserSerializer(request.user).data)
