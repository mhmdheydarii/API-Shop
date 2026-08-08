from django.contrib import admin
from .models import ProductModel, CategoryModel

# Register your models here.

@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "price", "discount_percent", "stock", "status"]
    search_fields = ["name"]

@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]

