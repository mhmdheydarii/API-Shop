from django.contrib import admin
from .models import User, Profile 

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "is_staff", "is_active", "is_verified" ,"type", "created_date"]

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name", "created_date"]
    search_fields = ["first_name"]

    