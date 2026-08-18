from django.urls import path
from . import views


app_name = "customer"

urlpatterns = [
    # Profile
    path("profile/", views.CustomerProfileView.as_view(), name="profile"),

    # Orders
    path("orders/", views.CustomerOrdersView.as_view(), name="orders"),
    path("order/<int:pk>/detail/", views.CustomerOrderDetailView.as_view(), name="order-detail"),
]