from rest_framework import serializers
from .models import CartModel, CartItemModel

class AddProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItemModel
        fields = ["product", "quantity"] 