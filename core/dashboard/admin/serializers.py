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