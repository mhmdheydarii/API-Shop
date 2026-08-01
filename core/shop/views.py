from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .serializers import ProductListSerializer, ProductDetailSerializer
from .models import ProductModel

# Create your views here.

class ProductsListView(APIView):

    allowed_ordering = ["-price", "price", "-created_date", "created_date"]

    def get(self, request):

        products = ProductModel.objects.filter(status=True)

        if search := request.query_params.get("search"):
            products = products.filter(name__icontains=search)
        if category := request.query_params.get("category"):
            products = products.filter(category__slug=category)
        if order_by := request.query_params.get("order_by"):
            if order_by not in self.allowed_ordering:
                return Response({"detail": "Invalid ordering field."}, status=status.HTTP_400_BAD_REQUEST)
            products = products.order_by(order_by)

        serializer = ProductListSerializer(products, many=True)  
        return Response(serializer.data, status=status.HTTP_200_OK)

    


class ProductDetailView(APIView):

    serializer_class = ProductDetailSerializer

    def get(self, request, slug):
        produtc = get_object_or_404(ProductModel, slug=slug, status=True)
        serializer = ProductDetailSerializer(produtc)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
