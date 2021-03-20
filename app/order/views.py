from django.contrib.auth import get_user_model

from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Order
from order import serializers


class OrderViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin):
    serializer_class = serializers.OrderSerializer
    queryset = Order.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# class OrderViewSet(viewsets.ModelViewSet):
#     serializer_class = serializers.OrderSerializer
#     queryset = Order.objects.all()
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)

#     def get_queryset(self):
#         return self.queryset.filter(user=self.request.user).order_by('-id')

