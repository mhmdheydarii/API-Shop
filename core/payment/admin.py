from django.contrib import admin
from . models import PaymentModel

# Register your models here.

@admin.register(PaymentModel)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["id", "authority_id", "amount", "status", "created_date"]