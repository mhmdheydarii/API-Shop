from rest_framework import serializers
from accounts.models import Profile
from order.models import OrderItemModel, OrderModel
from shop.models import ProductModel


class CustomerProfileSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "email"]


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


class CustomerOrderSerializer(serializers.ModelSerializer):
    
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = OrderModel
        fields = [
            "id",
            "status",
            "total_price",
            "created_date",
            "order_items",
        ]


class CustomerOrderDetailSerializer(serializers.ModelSerializer):

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