from rest_framework import serializers, fields
from rest_framework.fields import Field

from .models import Product, Category, Cart, CartItem, Comment
from user.serializers import UserSerializer


class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class ChildCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title"]


class CategoryWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title", "sub_category"]


class CategoryReadSerializer(serializers.ModelSerializer):
    sub_category = ChildCategorySerializer(read_only=True)

    class Meta:
        model = Category
        fields = ["id", "title", "sub_category"]


class ProductSerializer(serializers.ModelSerializer):
    category = CategoryWriteSerializer()
    image = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "brand",
            "category",
            "size",
            "color",
            "original_price",
            "price",
            "stock",
            "description",
            "image",
            "create_date",
            "last_modified",
        ]

    def create(self, validated_data):
        validated_data["category"] = Category.objects.create(
            **validated_data.get("category", {})
        )
        product = Product.objects.create(**validated_data)
        return product


class ChildCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "user", "content", "create_date"]


class CommentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        get_reply_count = Field(source="get_reply_count")
        fields = [
            "id",
            "user",
            "product",
            "content",
            "reply",
            "get_reply_count",
            "create_date",
        ]


class CommentReadSerializer(serializers.ModelSerializer):
    reply = ChildCommentSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        get_reply_count = Field(source="get_reply_count")
        fields = [
            "id",
            "user",
            "product",
            "content",
            "reply",
            "get_reply_count",
            "create_date",
        ]


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity"]


class CartSerializer(serializers.ModelSerializer):
    products = CartItemSerializer(read_only=True, many=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Cart
        get_total = Field(source="get_total")
        get_tax_total = Field(source="get_tax_total")
        get_cart_total = Field(source="get_cart_total")
        fields = [
            "id",
            "user",
            "products",
            "get_total",
            "get_tax_total",
            "get_cart_total",
        ]


# class OrderItemSerializer(serializers.ModelSerializer):
#     product = serializers.PrimaryKeyRelatedField(
#         many=True,
#         queryset=Product.objects.all()
#     )
#     order = serializers.PrimaryKeyRelatedField(
#         many=True,
#         queryset=Order.objects.all()
#     )
#     date_added = serializers.SerializerMethodField()

#     class Meta:
#         model = OrderItem
#         fields = ['product', 'order', 'quantity', 'date_added']
#         read_only_fields = ('id',)

#     def get_date_added(self, obj):
#         return obj.date_added.strftime("%m/%d/%Y, %H:%M:%S")


# class OrderSerializer(serializers.ModelSerializer):
#     # user = serializers.SerializerMethodField(read_only=True)
#     order = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = Order
#         fields = '__all__'
#         read_only_fields = ('id',)

#     def get_order(self, obj):
#         orderitems = obj.orderitem_set.all()
#         serializer = OrderItemSerializer(orderitems, many=True)
#         return serializer.data

#     def get_user(self,obj):
#         user = obj.user
#         serializer = UserSerializer(user, many=False)
#         return serializer.data
