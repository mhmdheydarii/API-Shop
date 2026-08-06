from rest_framework import serializers
from .models import CartModel, CartItemModel
from shop.models import ProductModel


class AddProductSerializer(serializers.Serializer):

    product = serializers.PrimaryKeyRelatedField(queryset=ProductModel.objects.filter(status=True))


class UpdateProductSerializer(serializers.Serializer):

    product = serializers.PrimaryKeyRelatedField(queryset=ProductModel.objects.filter(status=True))
