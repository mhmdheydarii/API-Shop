from django.db import models
from accounts.validators import validate_iranian_cellphone_number

# Create your models here.


class ContactModel(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=12, validators=[validate_iranian_cellphone_number])
    message = models.TextField()

    class ContactStatusTypeModel(models.TextChoices):
            PENDING = "pending", "در انتظار بررسی"
            IN_PROGRESS = "in_progress", "درحال بررسی"
            RESOLVED = "resolved", "حل شده"
            CANCLED = "cancled", "کنسل شده"

    status = models.CharField(choices=ContactStatusTypeModel.choices, default=ContactStatusTypeModel.PENDING, max_length=20)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ["-created_date"]



class NewsLetterModel(models.Model):
    email = models.EmailField()

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ["-created_date"]
    