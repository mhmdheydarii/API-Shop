from django.contrib import admin
from .models import OrderModel, OrderItemModel

# Register your models here.

@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "full_name", "state", "city", "status", "created_date"]
    list_filter = ["state"]
    search_fields = ["city"]

@admin.register(OrderItemModel)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["id", "order", "product", "quantity", "price", "created_date"]