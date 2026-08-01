from rest_framework import serializers
from .models import ProductModel


class ProductListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductModel
        fields = [
            "id",
            "name",
            "slug",
            "image",
            "price",
            "discount_percent",
            "stock",
            "category",
            "created_date",
        ]


class ProductDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductModel
        fields = [
            "id",
            "name",
            "slug",
            "brief_description",
            "description",
            "image",
            "price",
            "discount_percent",
            "stock",
            "category",
            "created_date",
        ]


    def validate_price(self, price):
        if price <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return price
