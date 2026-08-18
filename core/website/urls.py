from django.urls import path
from . import views

app_name = "website"

urlpatterns = [
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("news-letter/", views.NewsLetterView.as_view(), name="news-letter")
]