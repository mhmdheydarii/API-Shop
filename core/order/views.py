from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import ScopedRateThrottle
from decimal import Decimal

from cart.models import CartModel
from .serializers import CheckOutSerializer
from .models import OrderItemModel
from .permissions import HasCustomerPermissions
from payment.zarinpal import ZarinPalSandbox
from payment.models import PaymentModel
# Create your views here.

class CheckOutView(APIView):

    permission_classes = [HasCustomerPermissions]
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
        return self.create_payment_url(order_obj)

    def create_payment_url(self, order):

        zarinpal = ZarinPalSandbox()
        response = zarinpal.payment_request(order.total_price)
        print("RESPONSE",response)
        authority_id = response.get("data",{}).get("authority")

        if not authority_id:
            return Response({"message":"Your authority is wrong"}, status=status.HTTP_400_BAD_REQUEST)

        payment_obj = PaymentModel.objects.create(
            authority_id=authority_id,
            amount=order.total_price
        )
        order.payment = payment_obj
        order.save()
        return Response(
            {
                "message":"You`r sended to payment page",
                "payment_url":zarinpal.generate_payment_url(authority_id)
            },
            status=status.HTTP_200_OK)