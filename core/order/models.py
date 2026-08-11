from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from accounts.models import User
from accounts.validators import validate_iranian_cellphone_number
from shop.models import ProductModel
from payment.models import PaymentModel
# Create your models here.

class CouponModel(models.Model):

    code = models.CharField(max_length=255)
    used_by = models.ManyToManyField(User, related_name="coupon_user", blank=True)
    max_limit_usage = models.PositiveIntegerField(default=0)
    discount_percent = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    expired_date = models.DateTimeField(default=timezone.now())
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

    class Meta:
        ordering = ["-created_date"]



class OrderModel(models.Model):

    class OrderStatusTypeModel(models.TextChoices):
        PENDING = "pending", "در انتظار"
        PAID = "paid", "پرداخت شده"
        CANCELED = "canceled", "لغو شده"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_order")

    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=12, validators=[validate_iranian_cellphone_number])
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    address = models.TextField()
    zip_code = models.CharField(max_length=50)

    total_price = models.DecimalField(default=0, max_digits=10, decimal_places=0)
    coupon = models.ForeignKey(CouponModel, on_delete=models.SET_NULL, null=True, blank=True, related_name="order_coupon")
    payment = models.ForeignKey(PaymentModel, on_delete=models.SET_NULL, null=True, blank=True)

    status = models.CharField(max_length=255, choices=OrderStatusTypeModel.choices, default=OrderStatusTypeModel.PENDING)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email  

    def calculate_total_price(self):
        return sum(item.price * item.quantity for item in self.order_items.all())

    class Meta:
        ordering = ["-created_date"]


class OrderItemModel(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name="order_items")

    product = models.ForeignKey(ProductModel, on_delete=models.SET_NULL, related_name="order_products", null=True)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=0)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order.user.email

    class Meta:
        ordering = ["-created_date"]
    
    