from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .serializers import (
    CustomerProfileSerializer, 
    CustomerOrderSerializer, 
    CustomerOrderDetailSerializer, 
    )
from ..permissions import HasCustomerPermission
from ..paginations import Pagination
from order.models import OrderModel


class CustomerProfileView(APIView):

    permission_classes = [HasCustomerPermission]

    def get(self, request):
        profile = request.user.user_profile
        serializer = CustomerProfileSerializer(profile)
        return Response(serializer.data)

    def patch(self, request):
        serializer = CustomerProfileSerializer(
            data=request.data, instance=request.user.user_profile, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Profile Information Updated", "data": serializer.data},
            status=status.HTTP_200_OK,
        )


class CustomerOrdersView(ListAPIView):

    permission_classes = [HasCustomerPermission]
    serializer_class = CustomerOrderSerializer
    pagination_class = Pagination

    def get_queryset(self):
        return OrderModel.objects.filter(status=OrderModel.OrderStatusTypeModel.PAID)
    

class CustomerOrderDetailView(APIView):

    permission_classes = [HasCustomerPermission]

    def get(self, request, pk):
        order = get_object_or_404(
            OrderModel,
            id=pk,
            user=request.user,
            status=OrderModel.OrderStatusTypeModel.PAID
        )
        serializer = CustomerOrderDetailSerializer(order)
        return Response(serializer.data)