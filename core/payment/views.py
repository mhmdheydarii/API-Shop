from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from .models import PaymentModel
from order.models import OrderModel
from .zarinpal import ZarinPalSandbox
from shop.models import ProductModel
from cart.models import CartModel
from cart.cart import CartSession
from order.permissions import HasCustomerPermissions
# Create your views here.

class VerifyPaymentview(APIView):

    permission_classes = [HasCustomerPermissions]

    def get(self, request):
        authority_id = request.query_params.get("Authority")
        payment_status = request.query_params.get("Status")
        payment_obj = get_object_or_404(PaymentModel, authority_id=authority_id)
        order = get_object_or_404(OrderModel, payment=payment_obj)

        if payment_status != "OK":
            payment_obj.status = payment_obj.StatusPaymentType.CANCELED
            payment_obj.save(update_fields=["status"])
            order.status = order.OrderStatusTypeModel.CANCELED
            order.save(update_fields=["status"])
            return Response({"message":"Payment failed. Please try again."}, status=status.HTTP_400_BAD_REQUEST)
        
        if payment_obj.status == payment_obj.StatusPaymentType.PAID:
            return Response({"message":"Payment has already been completed."}, status=status.HTTP_409_CONFLICT)

        zarinpal = ZarinPalSandbox()
        response = zarinpal.payment_verify(int(payment_obj.amount), authority_id)

        data = response.get("data",{})

        if data.get("code") == 100:

            try:
                with transaction.atomic():

                    for item in order.order_items.all():
                        product = ProductModel.objects.select_for_update().get(
                            id = item.product.id
                        )

                        if product.stock < item.quantity:
                            raise ValueError("Insufficient stock")

                        product.stock -= item.quantity
                        product.save()
            except ValueError:
                return Response({"message":"Insufficient stock for one or more products."}, status=status.HTTP_400_BAD_REQUEST)
            
            payment_obj.ref_id = data.get("ref_id")
            payment_obj.response_code = data.get("code")
            payment_obj.response_json = response
            payment_obj.status = payment_obj.StatusPaymentType.PAID
            payment_obj.save()
            order.status = order.OrderStatusTypeModel.PAID
            order.save()

            if order.coupon:
                order.coupon.used_by.add(order.user)
            cart = CartModel.objects.get(user=order.user)
            cart.cart_items.all().delete()
            CartSession(request.session).clear()
            return Response({"message":"Payment completed successfully."})

        else:
            payment_obj.ref_id = data.get("ref_id")
            payment_obj.response_code = data.get("code")
            payment_obj.response_json = response
            payment_obj.status = payment_obj.StatusPaymentType.CANCELED
            payment_obj.save()
            order.status = order.OrderStatusTypeModel.CANCELED
            order.save()

            return Response({"message":"Payment was canceled."})


        

        