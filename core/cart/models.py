from django.db import models
from accounts.models import User
from shop.models import ProductModel
# Create your models here.

class CartModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_cart")

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

    def calculate_total_price(self):
        return sum(item.product.get_price() * item.quantity for item in self.cart_items.all())

    class Meta:
        ordering = ["-created_date"]


class CartItemModel(models.Model):
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(ProductModel, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=0)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name

    class Meta:
        ordering = ["-created_date"]
    