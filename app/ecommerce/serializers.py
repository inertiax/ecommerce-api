from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, Category




# class RegistrationSerializer(serializers.Serializer):
#     email = serializers.CharField(max_length=50)
#     password = serializers.CharField(
#         style={'input_type': 'password'},
#         trim_whitespace=False
#     )

#     def validate(self, attrs):
#         email = attrs.get('email')
#         password = attrs.get('password')

#         user = authenticate(
#             request=self.context.get('request'),
#             username=email,
#             password=password
#         )
#         if not user:
#             msg = _('Unable to authentication')
#             raise serializers.ValidationError(msg, code='authentication')

#         attrs['user'] = user
#         return attrs


class UserSerializer(serializers.HyperlinkedModelSerializer):
    products = serializers.PrimaryKeyRelatedField(many=True, queryset=Product.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'products']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """validate and auth the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    # create_date = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    # last_modified = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    user = serializers.ReadOnlyField(source='user.username', read_only=False)
    
    class Meta:
        model = Product
        fields = ['id', 'user', 'name', 'brand', 'category', 'size', 'color', 'price',
                  'stock', 'description', 'create_date', 'last_modified']
