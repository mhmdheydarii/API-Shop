from django.db import models
from accounts.models import User
from cart.models import CartModel
from accounts.validators import validate_iranian_cellphone_number
from shop.models import ProductModel
# Create your models here.


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
        return self.order

    class Meta:
        ordering = ["-created_date"]
    
    