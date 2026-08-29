from django.shortcuts import get_object_or_404
from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import PaymentModel
from .zarinpal import ZarinPalSandbox

from order.models import OrderModel
from shop.models import ProductModel
from cart.models import CartModel
from cart.cart import CartSession


class VerifyPaymentView(APIView):

    def get(self, request):
        authority = request.query_params.get("Authority")
        payment_status = request.query_params.get("Status")

        if not authority:
            return Response(
                {"message": "Invalid payment authority."},
                status=status.HTTP_400_BAD_REQUEST
            )

        payment = get_object_or_404(
            PaymentModel,
            authority_id=authority
        )

        order = get_object_or_404(
            OrderModel,
            payment=payment
        )

        if payment_status != "OK":
            with transaction.atomic():
                payment = PaymentModel.objects.select_for_update().get(
                    pk=payment.pk
                )

                if payment.status == payment.StatusPaymentType.PAID:
                    return Response(
                        {"message": "Payment has already been completed."},
                        status=status.HTTP_409_CONFLICT
                    )

                payment.status = payment.StatusPaymentType.CANCELED
                payment.save(update_fields=["status"])

                order.status = order.OrderStatusTypeModel.CANCELED
                order.save(update_fields=["status"])

            return Response(
                {"message": "Payment failed. Please try again."},
                status=status.HTTP_400_BAD_REQUEST
            )


        zarinpal = ZarinPalSandbox()

        response = zarinpal.payment_verify(
            int(payment.amount),
            authority
        )

        data = response.get("data", {})
        code = data.get("code")


        if code == 100:

            try:
                with transaction.atomic():

                    payment = PaymentModel.objects.select_for_update().get(
                        pk=payment.pk
                    )

                    if payment.status == payment.StatusPaymentType.PAID:
                        return Response(
                            {"message": "Payment has already been completed."},
                            status=status.HTTP_409_CONFLICT
                        )

                    for item in order.order_items.all():

                        product = ProductModel.objects.select_for_update().get(
                            pk=item.product_id
                        )

                        if product.stock < item.quantity:
                            raise ValueError(
                                "Insufficient stock"
                            )

                        product.stock -= item.quantity

                        product.save(
                            update_fields=["stock"]
                        )

                    payment.ref_id = data.get("ref_id")
                    payment.response_code = code
                    payment.response_json = response
                    payment.status = payment.StatusPaymentType.PAID

                    payment.save()

                    order.status = order.OrderStatusTypeModel.PAID
                    order.save(update_fields=["status"])

                    if order.coupon:
                        order.coupon.used_by.add(order.user)

                    cart = CartModel.objects.get(
                        user=order.user
                    )

                    cart.cart_items.all().delete()

            except ValueError:
                return Response(
                    {
                        "message":
                        "Insufficient stock for one or more products."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            CartSession(request.session).clear()

            return Response(
                {"message": "Payment completed successfully."},
                status=status.HTTP_200_OK
            )

        elif code == 101:

            return Response(
                {"message": "Payment has already been completed."},
                status=status.HTTP_200_OK
            )

        else:

            with transaction.atomic():

                payment = PaymentModel.objects.select_for_update().get(
                    pk=payment.pk
                )

                if payment.status == payment.StatusPaymentType.PAID:
                    return Response(
                        {"message": "Payment has already been completed."},
                        status=status.HTTP_409_CONFLICT
                    )

                payment.ref_id = data.get("ref_id")
                payment.response_code = code
                payment.response_json = response
                payment.status = payment.StatusPaymentType.CANCELED

                payment.save()

                order.status = order.OrderStatusTypeModel.CANCELED
                order.save(update_fields=["status"])

            return Response(
                {"message": "Payment was canceled."},
                status=status.HTTP_400_BAD_REQUEST
            )
