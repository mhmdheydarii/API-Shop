from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import CheckOutSerializer
from cart.models import CartModel
from .models import OrderItemModel
# Create your views here.

class CheckOutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CheckOutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        order_obj = serializer.save(user=user)

        cart = CartModel.objects.get(user=user)
        for cart_item in cart.cart_items.all():
            OrderItemModel.objects.create(
                order = order_obj,
                product = cart_item.product,
                quantity = cart_item.quantity,
                price = cart_item.product.get_price(),
            )
        order_obj.total_price = order_obj.calculate_total_price()
        order_obj.save()
        return Response({"message":"Address added and order created successfully"}, status=status.HTTP_200_OK)
