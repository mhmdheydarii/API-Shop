from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.filters import OrderingFilter, SearchFilter
from django.shortcuts import get_object_or_404
from django.core.cache import cache

from order.models import OrderModel, CouponModel
from payment.models import PaymentModel
from shop.models import ProductModel, CategoryModel
from website.models import TicketModel
from ..permissions import HasAdminPermission
from ..paginations import Pagination
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
    AdminCategoriesSerializer,
    AdminCategoryDetailSerializer,
    AdminTicketsSerializer,
    AdminTicketDetailSerializer,
    )

class AdminProfileView(APIView):

    permission_classes = [HasAdminPermission]

    def get(self, request):
        profile = request.user.user_profile

        cache_key = f"admin_profile:{profile.id}"
        admin_profile_data = cache.get(cache_key)

        if admin_profile_data is not None:
            return Response(admin_profile_data)

        serializer = AdminProfileSerializer(profile)
        cache.set(cache_key, serializer.data, 60*15)

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
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ["total_price", "created_date"]
    ordering = ["-created_date"]
    search_fields = ["state"]
    pagination_class = Pagination

    def get_queryset(self):
        orders = OrderModel.objects.all()

        if status_type := self.request.query_params.get("status"):
            orders = orders.filter(status=status_type)

        return orders

    def list(self, request, *args, **kwargs):
        cache_key = f"admin_orders:{request.get_full_path()}"
        admin_orders_data = cache.get(cache_key)

        if admin_orders_data is not None:
            return Response(admin_orders_data)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, 60*15)

        return response

    

class AdminOrderDetailView(APIView):

    permission_classes = [HasAdminPermission]

    def get(self, request, pk):
        cache_key = f"admin_order:{pk}"
        admin_order_data = cache.get(cache_key)

        if admin_order_data is not None:
            return Response(admin_order_data)

        order = get_object_or_404(
            OrderModel,
            id=pk
        )
        serializer = AdminOrderDetailSerializer(order)
        cache.set(cache_key, serializer.data, 60*15)

        return Response(serializer.data)



class AdminCouponListView(ListCreateAPIView):

    permission_classes = [HasAdminPermission]
    serializer_class = AdminCouponSerializer
    pagination_class = Pagination

    def get_queryset(self):
        return CouponModel.objects.all()

    def list(self, request, *args, **kwargs):
        cache_key = f"admin_coupons:{request.get_full_path()}"
        admin_coupons_data = cache.get(cache_key)

        if admin_coupons_data is not None:
            return Response(admin_coupons_data)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, 60*15)

        return response


class AdminCouponDetailView(APIView):

    permission_classes = [HasAdminPermission]

    def get(self, request, slug):
        cache_key = f"admin_coupon:{slug}"
        admin_coupon_data = cache.get(cache_key)

        if admin_coupon_data is not None:
            return Response(admin_coupon_data)

        coupon = get_object_or_404(
            CouponModel,
            slug=slug
        )
        serializer = AdminCouponDetailSerializer(coupon)
        cache.set(cache_key, serializer.data, 60*15)
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
    pagination_class = Pagination

    def get_queryset(self):
        return PaymentModel.objects.all()

    def list(self, request, *args, **kwargs):
        cache_key = f"admin_payments:{request.get_full_path()}"
        admin_payments_data = cache.get(cache_key)

        if admin_payments_data is not None:
            return Response(admin_payments_data)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, 60*15)

        return response



class AdminPaymentDetailView(APIView):

    permission_classes = [HasAdminPermission]

    def get(self, request, pk):
        cache_key = f"admin_payment:{pk}"
        admin_payment_data = cache.get(cache_key)

        if admin_payment_data is not None:
            return Response(admin_payment_data)

        payment = get_object_or_404(
            PaymentModel,
            id=pk 
        )
        serializer = AdminPaymentDetialSerializer(payment)
        cache.set(cache_key, serializer.data, 60*15)

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
    pagination_class = Pagination

    def get_queryset(self):
        return ProductModel.objects.all()

    def list(self, request, *args, **kwargs):
        cache_key = f"admin_products:{request.get_full_path()}"
        admin_products_data = cache.get(cache_key)

        if admin_products_data is not None:
            return Response(admin_products_data)
        
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, 60*15)

        return response

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
        cache_key = f"admin_product:{slug}"
        admin_product_data = cache.get(cache_key)

        if admin_product_data is not None:
            return Response(admin_product_data)
        
        product = get_object_or_404(
            ProductModel,
            slug=slug,
        )

        serializer = AdminProductDetailSerializer(product)
        cache.set(cache_key, serializer.data, 60*15)

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



class AdminCategoriesView(ListAPIView):

    permission_classes = [HasAdminPermission]
    serializer_class = AdminCategoriesSerializer
    pagination_class = Pagination

    def get_queryset(self):
        return CategoryModel.objects.all()

    def list(self, request, *args, **kwargs):
        cache_key = f"admin_categories:{request.get_full_path()}"
        admin_categories_data = cache.get(cache_key)

        if admin_categories_data is not None:
            return Response(admin_categories_data)
        
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, 60*15)

        return response


class AdminCategoryDetailView(APIView):

    permission_classes = [HasAdminPermission]

    def get(self, request, slug):
        cache_key = f"admin_category:{slug}"
        admin_category_data = cache.get(cache_key)

        if admin_category_data is not None:
            return Response(admin_category_data)
        
        category = get_object_or_404(
            CategoryModel,
            slug=slug
        )
        serializer = AdminCategoryDetailSerializer(category)
        cache.set(cache_key, serializer.data, 60*15)

        return Response(serializer.data)

    def patch(self, request, slug):
        category = get_object_or_404(
            CategoryModel,
            slug=slug
        )
        serializer = AdminCategoryDetailSerializer(category, partial=True, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, slug):
        category = get_object_or_404(
            CategoryModel,
            slug=slug
        )
        category.delete()
        return Response({"message":"Category deleted successfully"}, status=status.HTTP_200_OK)


class TicketsView(ListAPIView):

    permission_classes = [HasAdminPermission]
    serializer_class = AdminTicketsSerializer
    pagination_class = Pagination

    def get_queryset(self):
        return TicketModel.objects.all()

    def list(self, request, *args, **kwargs):
        cache_key = f"admin_tickets:{request.get_full_path()}"
        admin_tickets_data = cache.get(cache_key)

        if admin_tickets_data is not None:
            return Response(admin_tickets_data)
        
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, 60*15)

        return response


class TicketDetailView(APIView):

    permission_classes = [HasAdminPermission]

    def get(self, request, pk):
        cache_key = f"admin_ticket:{pk}"
        admin_tecket_data = cache.get(cache_key)

        if admin_tecket_data is not None:
            return Response(admin_tecket_data)
        
        ticket = get_object_or_404(
            TicketModel,
            id=pk
        )
        serializer = AdminTicketDetailSerializer(ticket)
        cache.set(cache_key, serializer.data, 60*15)
        
        return Response(serializer.data)

    def patch(self, request, pk):
        ticket = get_object_or_404(
            TicketModel,
            id=pk
        )
        serializer = AdminTicketDetailSerializer(ticket, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)