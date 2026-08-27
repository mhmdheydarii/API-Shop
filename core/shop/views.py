from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_control
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
import time
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

    @method_decorator(cache_page(60*15, key_prefix="product_list"))
    @method_decorator(cache_control(private=False, no_cache=True))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    

    


class ProductDetailView(APIView):

    serializer_class = ProductDetailSerializer

    def get(self, request, slug):
        produtc = get_object_or_404(ProductModel, slug=slug, status=True)
        serializer = ProductDetailSerializer(produtc)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class RecentProductsView(APIView):

    def get(self, request):
        products = ProductModel.objects.filter(status=True)[:4]
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)


class DiscountedProductsView(APIView):

    def get(self, request):
        products = ProductModel.objects.filter(status=True, discount_percent__gte=50)[:5]
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)