from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from django.shortcuts import get_object_or_404
from django.core.cache import cache

from .serializers import ProductListSerializer, ProductDetailSerializer
from .models import ProductModel
from .paginations import ProductsPagination

# Create your views here.

class ProductsListView(ListAPIView):

    serializer_class = ProductListSerializer
    pagination_class = ProductsPagination
    filter_backends = [OrderingFilter, SearchFilter]

    ordering_fields = ["price", "created_date"]
    ordering = ["-created_date"]
    search_fields = ["name"]

    def get_queryset(self):
        products = ProductModel.objects.filter(status=True).select_related("category")
        if category := self.request.query_params.get("category"):
            products = products.filter(category__slug=category)
        return products

    def list(self, request, *args, **kwargs):
        cache_key = f"product_list:{request.get_full_path()}"
        products_data = cache.get(cache_key)

        if products_data is not None:
            return Response(products_data)
        
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, 60*15)
        return response

    


class ProductDetailView(APIView):

    serializer_class = ProductDetailSerializer

    def get(self, request, slug):
        cache_key = f"product_detail:{slug}"
        product_data = cache.get(cache_key)

        if product_data is not None:
            return Response(product_data)

        produtc = get_object_or_404(
            ProductModel.objects.select_related("category"),
            slug=slug, 
            status=True
            )
        serializer = ProductDetailSerializer(produtc)

        cache.set(cache_key, serializer.data, 60 * 15)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class RecentProductsView(APIView):

    def get(self, request):
        cache_key = "recent_products"
        recent_products_data = cache.get(cache_key)

        if recent_products_data is not None:
            return Response(recent_products_data)
        
        products = ProductModel.objects.filter(status=True).select_related("category")[:4]
        serializer = ProductListSerializer(products, many=True)

        cache.set(cache_key, serializer.data, 60 * 15)
        return Response(serializer.data)


class DiscountedProductsView(APIView):

    def get(self, request):
        cache_key = "discounted_products"
        discounted_products_data = cache.get(cache_key)

        if discounted_products_data is not None:
            return Response(discounted_products_data)
        
        products = ProductModel.objects.filter(
            status=True, 
            discount_percent__gte=50).select_related("category")[:5]
        serializer = ProductListSerializer(products, many=True)

        cache.set(cache_key, serializer.data, 60 * 15)
        return Response(serializer.data)