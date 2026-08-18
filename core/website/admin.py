from django.contrib import admin
from .models import ContactModel, NewsLetterModel
# Register your models here.

@admin.register(ContactModel)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "created_date"]


@admin.register(NewsLetterModel)
class NewsLetterAdmin(admin.ModelAdmin):
    list_display = ["email", "created_date"]
