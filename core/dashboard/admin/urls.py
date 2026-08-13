from django.urls import path
from . import views

app_name = "admin"

urlpatterns = [
    path("profile/", views.AdminProfileView.as_view(), name="profile")
]