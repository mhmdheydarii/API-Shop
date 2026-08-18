from django.urls import path, re_path
from . import views

app_name = "admin"

urlpatterns = [
    # Profile
    path("profile/", views.AdminProfileView.as_view(), name="profile"),

    # Orders
    path("orders/", views.AdminOrdersView.as_view(), name="orders"),
    path("order/<int:pk>/detail/", views.AdminOrderDetailView.as_view(), name="order-detail"),

    # Coupons
    path("coupons/", views.AdminCouponListView.as_view(), name="coupon-list"),
    path("coupon/<slug:slug>/detail/", views.AdminCouponDetailView.as_view(), name="coupon-detail"),

    # Payments
    path("payments/", views.AdminPaymentsView.as_view(), name="payments"),
    path("payment/<int:pk>/detail/", views.AdminPaymentDetailView.as_view(), name="payment-detail"),

    # Procuts
    path("products/", views.AdminProductsView.as_view(), name="products"),
    path("product/create/", views.AdminProductCreateView.as_view(), name="product-create"),
    re_path(r'product/(?P<slug>[-\w]*)/detail/', views.AdminProductDetialView.as_view(), name="product-detail"),

    # Categories
    path("categories/", views.AdminCategoriesView.as_view(), name="categories"),
    re_path(r'category/(?P<slug>[-\w]*)/detail/', views.AdminCategoryDetailView.as_view(), name="category-detail"),

    # Tickets
]