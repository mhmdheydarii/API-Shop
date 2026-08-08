from rest_framework import serializers
from .models import OrderModel


class CheckOutSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderModel
        fields = ["full_name", "phone_number", "state", "city", "address", "zip_code"]

    