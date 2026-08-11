from django.db import models
from django.db.models import JSONField
# Create your models here.

class PaymentModel(models.Model):
    authority_id = models.CharField(max_length=255)
    amount = models.DecimalField(default=0, max_digits=10, decimal_places=0)
    ref_id = models.BigIntegerField(default=0, null=True, blank=True)
    response_json = JSONField(default=dict)
    response_code = models.IntegerField(null=True, blank=True)

    class StatusPaymentType(models.TextChoices):
        PENDING = "pending", "در انتظار پرداخت"
        PAID = "paied", "پرداخت شده"
        CANCELED = "canceled", "لغو شده"

    status = models.CharField(max_length=20, choices=StatusPaymentType.choices, default=StatusPaymentType.PENDING)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.authority_id

    class Meta:
        ordering = ["-created_date"]

