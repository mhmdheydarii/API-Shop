from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.cache import cache

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

        cache_key = f"customer_profile:{profile.id}"
        customer_profile_data = cache.get(cache_key)

        if customer_profile_data is not None:
            return Response(customer_profile_data)
        
        serializer = CustomerProfileSerializer(profile)
        cache.set(cache_key, serializer.data, 60*15)

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
        return OrderModel.objects.filter(
            user=self.request.user,
            status=OrderModel.OrderStatusTypeModel.PAID
        )

    def list(self, request, *args, **kwargs):
        cache_key = f"customer_orders:{request.user.id}_{request.get_full_path()}"
        customer_orders_data = cache.get(cache_key)

        if customer_orders_data is not None:
            return Response(customer_orders_data)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, 60*15)

        return response
    

class CustomerOrderDetailView(APIView):

    permission_classes = [HasCustomerPermission]

    def get(self, request, pk):
        cache_key = f"customer_order:{request.user.id}_{pk}"
        customer_order_data = cache.get(cache_key)

        if customer_order_data is not None:
            return Response(customer_order_data)
        
        order = get_object_or_404(
            OrderModel,
            id=pk,
            user=request.user,
            status=OrderModel.OrderStatusTypeModel.PAID
        )
        
        serializer = CustomerOrderDetailSerializer(order)
        cache.set(cache_key, serializer.data, 60*15)

        return Response(serializer.data)