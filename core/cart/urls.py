from django.urls import path
from . import views


app_name = "cart"

urlpatterns = [
    path("add-product/", views.AddProductView.as_view(), name="add-product"),
    path("update-product/", views.UpdateProductView.as_view(), name="update-product"),
    path("remove-product/", views.RemoveProductView.as_view(), name="remove-product"),
]