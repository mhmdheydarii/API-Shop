from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .serializers import ProductListSerializer, ProductDetailSerializer
from .models import ProductModel
from .paginations import ProductsPagination

# Create your views here.

class ProductsListView(ListAPIView):

    serializer_class = ProductListSerializer
    pagination_class = ProductsPagination
    allowed_ordering = ["-price", "price", "-created_date", "created_date"]

    def get_queryset(self):

        products = ProductModel.objects.filter(status=True).select_related("category")

        if search := self.request.query_params.get("search"):
            products = products.filter(name__icontains=search)
        if category := self.request.query_params.get("category"):
            products = products.filter(category__slug=category)
        if order_by := self.request.query_params.get("order_by"):
            if order_by not in self.allowed_ordering:
                return ProductModel.objects.none()
            products = products.order_by(order_by)

        return products

    


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