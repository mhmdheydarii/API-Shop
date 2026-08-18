from django.urls import path
from . import views

app_name = "website"

urlpatterns = [
    path("ticket/", views.TicketView.as_view(), name="ticket"),
    path("news-letter/", views.NewsLetterView.as_view(), name="news-letter")
]