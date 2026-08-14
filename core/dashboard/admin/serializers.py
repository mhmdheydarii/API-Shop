from rest_framework import serializers
from accounts.models import Profile
from shop.models import ProductModel
from order.models import OrderModel, OrderItemModel


class AdminProfileSerializer(serializers.ModelSerializer):

    email = serializers.CharField(source="user.email", read_only=True)
    user_type = serializers.CharField(source="user.get_type_display", read_only=True)

    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "image",
            "email",
            "user_type"
        ]



class AdminOrderSerializer(serializers.ModelSerializer):
    
    user = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = OrderModel
        fields = [
            "id",
            "user",
            "total_price",
            "coupon",
            "state",
            "status",
            "created_date"
        ]


# Serializer for displaying order product details.
class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductModel
        fields = ["name", "image"]


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = OrderItemModel
        fields = ["product", "quantity", "price"]


class AdminOrderDetailSerializer(serializers.ModelSerializer):

    order_items = OrderItemSerializer(read_only=True, many=True)

    class Meta:
        model = OrderModel
        fields = [
            "full_name",
            "order_items",
            "phone_number",
            "state",
            "city",
            "address",
            "zip_code",
            "total_price",
            "coupon",
            "status",
            "created_date"
        ]