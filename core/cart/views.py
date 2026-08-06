from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .serializers import CartProductSerializer
from .cart import CartSession
from shop.models import ProductModel
# Create your views here.

class AddProductView(APIView):

    def post(self, request):
        cart = CartSession(request.session)
        serializer = CartProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data["product"]

        product_stock = product.stock

        result = cart.add_product(product.id, product_stock)

        if not result:
            return Response({"message":"Product is out of stock"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message":"Product added successfully"})


class UpdateProductView(APIView):

    def patch(self, request):
        cart = CartSession(request.session)
        serializer = CartProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data["product"]

        result = cart.update_product_quantity(product.id)

        if not result:
            return Response({"message":"Product stock not enough"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message":"Product quantity updated"}, status=status.HTTP_200_OK)


class RemoveProductView(APIView):

    def delete(self, request):
        cart = CartSession(request.session)
        serializer = CartProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = serializer.validated_data["product"]

        result = cart.remove_product(product.id)

        if not result:
            return Response({"message":"Product not found"}, status=status.HTTP_404_NOT_FOUND)
            
        return Response({"message":"Product removed successfully"}, status=status.HTTP_200_OK)