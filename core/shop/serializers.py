from rest_framework import serializers
from .models import ProductModel


class ProductListSerializer(serializers.ModelSerializer):

    category = serializers.CharField(source="category.name", read_only=True)

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

    category = serializers.CharField(source="category.name", read_only=True)
    
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