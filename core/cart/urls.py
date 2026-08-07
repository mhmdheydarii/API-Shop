from django.urls import path
from . import views


app_name = "cart"

urlpatterns = [
    path("add-item/", views.AddProductView.as_view(), name="add-item"),
    path("update-item/", views.UpdateProductView.as_view(), name="update-item"),
    path("remove-item/", views.RemoveProductView.as_view(), name="remove-item"),
    path("items/", views.ProductListView.as_view(), name="cart-items"),
]