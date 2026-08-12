from rest_framework import serializers
from accounts.models import Profile
from order.models import OrderItemModel, OrderModel
from shop.models import ProductModel


class ProfileSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "email"]

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductModel
        fields = ["name", "image"]


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = OrderItemModel
        fields = ["product", "quantity", "price"]


class OrderSerializer(serializers.ModelSerializer):
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