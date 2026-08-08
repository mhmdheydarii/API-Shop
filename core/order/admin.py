from django.contrib import admin
from .models import CouponModel ,OrderModel, OrderItemModel

# Register your models here.

@admin.register(CouponModel)
class CouponAdmin(admin.ModelAdmin):
    list_display = ["code", "max_limit_usage", "discount_percent", "expired_date"]

@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "total_price", "coupon", "state", "status", "created_date"]
    list_filter = ["state"]
    search_fields = ["city"]

@admin.register(OrderItemModel)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["id", "order", "product", "quantity", "price", "created_date"]