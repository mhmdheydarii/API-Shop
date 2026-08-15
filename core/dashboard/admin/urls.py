from django.urls import path
from . import views

app_name = "admin"

urlpatterns = [
    # Profile
    path("profile/", views.AdminProfileView.as_view(), name="profile"),

    # Orders
    path("orders/", views.AdminOrdersView.as_view(), name="orders"),
    path("order/<int:pk>/detail/", views.AdminOrderDetailView.as_view(), name="order-detail"),

    # Coupon
    path("coupon/list/", views.AdminCouponListView.as_view(), name="coupon-list"),
    path("coupon/<slug:slug>/detial/", views.AdminCouponDetailView.as_view(), name="coupon-detial"),

    # Payment
    path("payments/", views.AdminPaymentsView.as_view(), name="payments"),
    path("payment/<int:pk>/detial/", views.AdminPaymentDetialView.as_view(), name="payment-detial"),
]