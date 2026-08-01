from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .serializers import ProductListSerializer, ProductDetailSerializer
from .models import ProductModel

# Create your views here.

class ProductsListView(APIView):
    
    def get(self, request):
        products = ProductModel.objects.filter(status=True)
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class ProductDetailView(APIView):

    serializer_class = ProductDetailSerializer

    def get(self, request, slug):
        produtc = get_object_or_404(ProductModel, slug=slug, status=True)
        serializer = ProductDetailSerializer(produtc)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, slug):
        product = get_object_or_404(ProductModel, slug=slug)
        serializer = ProductDetailSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, slug):
        product = get_object_or_404(ProductModel, slug=slug)
        product.delete()
        return Response({"detail":"product deleted"}, status=status.HTTP_200_OK)
    
