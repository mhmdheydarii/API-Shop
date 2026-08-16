from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from order.models import OrderModel, CouponModel
from payment.models import PaymentModel
from shop.models import ProductModel
from ..permissions import HasAdminPermission
from .paginations import AdminDashboardPagination
from .serializers import (
    AdminProfileSerializer, 
    AdminOrderSerializer, 
    AdminOrderDetailSerializer,
    AdminCouponSerializer,
    AdminCouponDetailSerializer,
    AdminPaymentSerializer,
    AdminPaymentDetialSerializer,
    AdminProductsSerializer,
    AdminProductCreateSerializer,
    AdminProductDetailSerializer,
    )

class AdminProfileView(APIView):

    permission_classes = [HasAdminPermission]

    def get(self, request):
        profile = request.user.user_profile
        serializer = AdminProfileSerializer(profile)
        return Response(serializer.data)

    def patch(self, request):
        serializer = AdminProfileSerializer(
            data=request.data, 
            instance=request.user.user_profile, 
            partial=True
            )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AdminOrdersView(ListAPIView):

    permission_classes = [HasAdminPermission]
    serializer_class = AdminOrderSerializer
    pagination_class = AdminDashboardPagination
    allowed_ordering = ["-total_price", "total_price", "-created_date", "created_date"]

    def get_queryset(self):
        orders = OrderModel.objects.all()

        if search := self.request.query_params.get("search"):
            orders = orders.filter(state__icontains=search)
        if status_type := self.request.query_params.get("status"):
            orders = orders.filter(status=status_type)
        if order_by := self.request.query_params.get("order_by"):
            if order_by not in self.allowed_ordering:
                return OrderModel.objects.none()
            orders = orders.order_by(order_by)

        return orders


class AdminOrderDetailView(APIView):

    permission_classes = [HasAdminPermission]

    def get(self, request, pk):
        order = get_object_or_404(
            OrderModel,
            id=pk
        )
        serializer = AdminOrderDetailSerializer(order)
        return Response(serializer.data)


class AdminCouponListView(ListCreateAPIView):

    permission_classes = [HasAdminPermission]
    serializer_class = AdminCouponSerializer
    pagination_class = AdminDashboardPagination

    def get_queryset(self):
        return CouponModel.objects.all()


class AdminCouponDetailView(APIView):

    permission_classes = [HasAdminPermission]

    def get(self, request, slug):
        coupon = get_object_or_404(
            CouponModel,
            slug=slug
        )
        serializer = AdminCouponDetailSerializer(coupon)
        return Response(serializer.data)

    def patch(self, request, slug):
        coupon = get_object_or_404(
            CouponModel,
            slug=slug
        )
        serializer = AdminCouponDetailSerializer(coupon ,data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, slug):
        coupon = get_object_or_404(
            CouponModel,
            slug=slug
        )
        coupon.delete()
        return Response({"message":"Coupon deleted successfully"}, status=status.HTTP_200_OK)



class AdminPaymentsView(ListAPIView):

    permission_classes = [HasAdminPermission]
    serializer_class = AdminPaymentSerializer
    pagination_class = AdminDashboardPagination

    def get_queryset(self):
        return PaymentModel.objects.all()



class AdminPaymentDetailView(APIView):

    permission_classes = [HasAdminPermission]

    def get(self, request, pk):
        payment = get_object_or_404(
            PaymentModel,
            id=pk 
        )
        serializer = AdminPaymentDetialSerializer(payment)
        return Response(serializer.data)

    def delete(self, request, pk):
        payment = get_object_or_404(
            PaymentModel,
            id=pk 
        )
        payment.delete()
        return Response({"message":"Payment deleted successfully"}, status=status.HTTP_200_OK)
    


class AdminProductsView(ListAPIView):

    permission_classes = [HasAdminPermission]
    serializer_class = AdminProductsSerializer
    pagination_class = AdminDashboardPagination

    def get_queryset(self):
        return ProductModel.objects.all()


class AdminProductCreateView(APIView):

    permission_classes = [HasAdminPermission]

    def post(self, request):
        serializer = AdminProductCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AdminProductDetialView(APIView):

    permission_classes = [HasAdminPermission]

    def get(self, request, slug):
        product = get_object_or_404(
            ProductModel,
            slug=slug,
        )
        serializer = AdminProductDetailSerializer(product)
        return Response(serializer.data)

    def patch(self, request, slug):
        product = get_object_or_404(
            ProductModel,
            slug=slug
        )
        serializer = AdminProductDetailSerializer(
            product,
            data=request.data,
            partial=True
            )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, slug):
        product = get_object_or_404(
            ProductModel,
            slug=slug
        )
        product.delete()
        return Response({"message":"Product deleted successfully"}, status=status.HTTP_200_OK)