from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .serializers import AddProductSerializer
from .cart import CartSession
from shop.models import ProductModel
# Create your views here.

class AddProductView(APIView):

    def post(self, request):
        cart = CartSession(request.session)
        serializer = AddProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data["product"]
        
        product_stock = product.stock

        result = cart.add_product(product.id, product_stock)

        if not result:
            return Response({"message":"Product is out of stock"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message":"Product added successfully"})