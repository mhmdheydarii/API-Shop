from django.urls import path
from . import views


app_name = "cart"

urlpatterns = [
    path("items/", views.CartItemsView.as_view(), name="cart-items"),
    path("item/", views.CartView.as_view(), name="cart-item"),
]