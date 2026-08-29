from django.urls import path
from . import views

app_name = "payment"

urlpatterns = [
    path("verify-peyment/", views.VerifyPaymentView.as_view(), name="verify-payment")
]