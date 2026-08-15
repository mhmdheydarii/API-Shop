from rest_framework import serializers
from accounts.models import Profile
from shop.models import ProductModel
from order.models import OrderModel, OrderItemModel, CouponModel
from accounts.models import User

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


class AdminCouponSerializer(serializers.ModelSerializer):

    class Meta:
        model = CouponModel
        fields = [
            "slug",
            "code",
            "max_limit_usage",
            "discount_percent",
            "expired_date",
            "created_date"
        ]


class CouponUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["email"]

class AdminCouponDetialSerializer(serializers.ModelSerializer):

    used_by = CouponUserSerializer(many=True ,read_only=True)

    class Meta:
        model = CouponModel
        fields = [
            "slug",
            "code",
            "used_by",
            "max_limit_usage",
            "discount_percent",
            "expired_date",
            "created_date"
        ]