from rest_framework import serializers
from .models import CartModel, CartItemModel
from shop.models import ProductModel


class CartProductSerializer(serializers.Serializer):

    product = serializers.PrimaryKeyRelatedField(queryset=ProductModel.objects.filter(status=True))