from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..permissions import HasAdminPermission
from .serializers import (
    AdminProfileSerializer, 
    AdminOrderSerializer, 
    AdminOrderDetailSerializer,
    AdminCouponSerializer,
    AdminCouponDetialSerializer,
    )
from order.models import OrderModel, CouponModel
from .paginations import AdminOrdersPagination

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
    pagination_class = AdminOrdersPagination
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


class AdminCouponListView(APIView):

    permission_classes = [HasAdminPermission]

    def get(self, request):
        coupon = CouponModel.objects.all()
        serializer = AdminCouponSerializer(coupon, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AdminCouponSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Coupon created successfully"}, status=status.HTTP_201_CREATED)


class AdminCouponDetailView(APIView):

    permission_classes = [HasAdminPermission]

    def get(self, request, slug):
        coupon = get_object_or_404(
            CouponModel,
            slug=slug
        )
        serializer = AdminCouponDetialSerializer(coupon)
        return Response(serializer.data)

    def patch(self, request, slug):
        coupon = get_object_or_404(
            CouponModel,
            slug=slug
        )
        serializer = AdminCouponDetialSerializer(coupon ,data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)