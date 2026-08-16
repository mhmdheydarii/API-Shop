from rest_framework import serializers
from accounts.models import Profile
from shop.models import ProductModel
from order.models import OrderModel, OrderItemModel, CouponModel
from accounts.models import User
from payment.models import PaymentModel
from shop.models import ProductModel

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
            "id",
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
            "created_date",
            "updated_date"
        ]


class AdminCouponSerializer(serializers.ModelSerializer):

    class Meta:
        model = CouponModel
        fields = [
            "id",
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


class AdminCouponDetailSerializer(serializers.ModelSerializer):

    used_by = CouponUserSerializer(many=True ,read_only=True)

    class Meta:
        model = CouponModel
        fields = [
            "id",
            "slug",
            "code",
            "used_by",
            "max_limit_usage",
            "discount_percent",
            "expired_date",
            "created_date",
            "updated_date"
        ]


class AdminPaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentModel
        fields = [
            "id",
            "authority_id",
            "amount",
            "status", 
            "created_date"
        ]


class AdminPaymentDetialSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentModel
        fields = [
            "authority_id",
            "amount",
            "ref_id",
            "response_json",
            "response_code",
            "status", 
            "created_date",
            "updated_date"
        ]



class AdminProductsSerializer(serializers.ModelSerializer):

    category = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = ProductModel
        fields = [
            "id",
            "name",
            "price",
            "discount_percent",
            "stock",
            "category",
            "status",
            "created_date"
        ]


class AdminProductCreateSerializer(serializers.ModelSerializer):

    category = serializers.CharField(source="category.name")

    class Meta:
        model = ProductModel
        fields = [
            "name",
            "slug",
            "brief_description",
            "description",
            "image",
            "price",
            "discount_percent",
            "stock",
            "category",
            "status",
        ]

class AdminProductDetailSerializer(serializers.ModelSerializer):

    category = serializers.CharField(source="category.name")
    
    class Meta:
        model = ProductModel
        fields = [
            "name",
            "slug",
            "brief_description",
            "description",
            "image",
            "price",
            "discount_percent",
            "stock",
            "category",
            "status",
            "get_price"
        ]