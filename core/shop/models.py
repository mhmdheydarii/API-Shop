from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal

# Create your models here.

class ProductModel(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, allow_unicode=True)
    brief_description = models.CharField(max_length=500)
    description = models.TextField()
    image = models.ImageField(upload_to="products/images")
    price = models.DecimalField(default=0, max_digits=10, decimal_places=0)
    discount_percent = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey("CategoryModel", on_delete=models.SET_NULL, related_name="products", null=True)
    status = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_price(self):
        discount_amount = (self.price * Decimal(self.discount_percent)) / Decimal(100)
        discounted_price = self.price - discount_amount
        return int(discounted_price)

    class Meta:
        ordering = ["-created_date"]

    

class CategoryModel(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, allow_unicode=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_date"]
