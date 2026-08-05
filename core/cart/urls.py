from django.urls import path
from . import views


app_name = "cart"

urlpatterns = [
    path("add-product/", views.AddProductView.as_view(), name="add-product"),
]