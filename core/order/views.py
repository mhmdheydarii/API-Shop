from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import ScopedRateThrottle

from .serializers import CheckOutSerializer
from cart.models import CartModel
from .models import OrderItemModel
from decimal import Decimal
# Create your views here.

class CheckOutView(APIView):

    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "checkout"

    def post(self, request):
        serializer = CheckOutSerializer(data=request.data, context={"request":request})
        serializer.is_valid(raise_exception=True)
        coupon = serializer.validated_data["coupon"]
        user = request.user
        order_obj = serializer.save(user=user)

        cart = CartModel.objects.get(user=user)

        if not cart.cart_items.exists():
            return Response({"message":"Cannot create order, Your cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
        
        for cart_item in cart.cart_items.all():
            OrderItemModel.objects.create(
                order = order_obj,
                product = cart_item.product,
                quantity = cart_item.quantity,
                price = cart_item.product.get_price(),
            )
        order_obj.total_price = order_obj.calculate_total_price()
        
        if coupon:
            discount_amount = (order_obj.total_price * Decimal(coupon.discount_percent) / Decimal("100"))
            order_obj.total_price -= discount_amount
            order_obj.coupon = coupon

        order_obj.save()
        return Response({"message":"Order created successfully"}, status=status.HTTP_200_OK)
