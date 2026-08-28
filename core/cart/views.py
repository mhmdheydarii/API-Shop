from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from django.core.cache import cache

from .serializers import CartProductSerializer
from .cart import CartSession

# Create your views here.


class CartItemsView(APIView):

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "cart_items"

    def get(self, request):
        cache_key = f"cart_items:{request.session.session_key}"
        cart_items_data = cache.get(cache_key)

        if cart_items_data is not None:
            return Response(cart_items_data)

        cart = CartSession(request.session)
        result = cart.get_product_item()
        payment_amount = cart.get_total_payment_amount()
        total_quantity = cart.get_total_quantity()

        if not result:
            return Response({"message":"Cart does`nt have any item"}, status=status.HTTP_200_OK)

        cache.set(cache_key, {
            "message":"Cart items retrieved successfully",
            "data":result, 
            "payment_amount":payment_amount, 
            "total_quantity":total_quantity
            }, 60*15)
        
        return Response({
                "message":"Cart items retrieved successfully",
                "data":result,
                "payment_amount":payment_amount,
                "total_quantity":total_quantity
            }, 
            status=status.HTTP_200_OK
            )


class CartView(APIView):

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "cart_operations"

    
    # Add product in cart
    def post(self, request):
        cart = CartSession(request.session)
        serializer = CartProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data["product"]

        product_stock = product.stock

        result = cart.add_product(product.id, product_stock)

        if not result:
            return Response({"message": "Cannot add product to cart. Product may be out of stock or unavailable."},
                            status=status.HTTP_400_BAD_REQUEST)
        if request.user.is_authenticated:
            cart.sync_session_cart_to_db(user=request.user)
        return Response({"message":"Product added successfully"})
    
    # Update product quantity in cart
    def patch(self, request):
        cart = CartSession(request.session)
        serializer = CartProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data["product"]

        result = cart.update_product_quantity(product.id)

        if not result:
            return Response({"message": "Product stock limit reached"}, status=status.HTTP_400_BAD_REQUEST)
        if request.user.is_authenticated:
            cart.sync_session_cart_to_db(user=request.user)
        return Response({"message":"Product quantity updated"}, status=status.HTTP_200_OK)
    
    # Delete product from cart
    def delete(self, request):
        cart = CartSession(request.session)
        serializer = CartProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = serializer.validated_data["product"]

        result = cart.remove_product(product.id)

        if not result:
            return Response({"message":"Product not found"}, status=status.HTTP_404_NOT_FOUND)
        if request.user.is_authenticated:
            cart.sync_session_cart_to_db(user=request.user)
        return Response({"message":"Product removed successfully"}, status=status.HTTP_200_OK)
