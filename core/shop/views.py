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

    def get(self, request, slug):
        produtc = get_object_or_404(ProductModel, slug=slug, status=True)
        serializer = ProductDetailSerializer(produtc)
        return Response(serializer.data, status=status.HTTP_200_OK)