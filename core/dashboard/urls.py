from django.urls import path, include
from . import views


app_name = "dashboard"

urlpatterns = [
    path("profile/", views.DashboardView.as_view(), name="profile"),

    # path("admin/", include("dashboard.admin.urls")),
    path("customer/", include("dashboard.customer.urls")),
]