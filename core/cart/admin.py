from django.contrib import admin
from .models import CartModel, CartItemModel

# Register your models here.

@admin.register(CartModel)
class CartAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "created_date", "updated_date"]

@admin.register(CartItemModel)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ["id", "cart", "product", "quantity", "created_date", "updated_date"]