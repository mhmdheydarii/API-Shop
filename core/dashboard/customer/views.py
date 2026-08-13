from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .serializers import ProfileSerializer, OrderSerializer, OrderDetailSerializer
from ..permissions import HasCustomerPermission
from order.models import OrderModel, OrderItemModel


class CustomerProfileView(APIView):

    permission_classes = [HasCustomerPermission]

    def get(self, request):
        profile = request.user.user_profile
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def patch(self, request):
        serializer = ProfileSerializer(
            data=request.data, instance=request.user.user_profile, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Profile Information Updated", "data": serializer.data},
            status=status.HTTP_200_OK,
        )


class CustomerOrdersView(APIView):

    permission_classes = [HasCustomerPermission]

    def get(self, request):
        orders = OrderModel.objects.filter(
            user=request.user, status=OrderModel.OrderStatusTypeModel.PAID
        ).prefetch_related("order_items")
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class CustomerOrderDetailView(APIView):

    permission_classes = [HasCustomerPermission]

    def get(self, request, pk):
        order = get_object_or_404(
            OrderModel,
            id=pk,
            user=request.user,
        )
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data)
