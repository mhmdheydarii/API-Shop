from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse
from accounts.models import UserType

# Create your views here.


class DashboardView(APIView):

    def get(self, request):

        if request.user.is_authenticated:
            if request.user.type in (UserType.admin.value, UserType.superuser.value):
                return Response(
                    {
                        "message": "User type is Admin",
                        "redirect_url": reverse("dashboard:admin:profile"),
                    }
                )
            
            if request.user.type in UserType.user.value:
                return Response(
                    {
                        "message": "User type is Customer",
                        "redirect_url": reverse("dashboard:customer:profile"),
                    }
                )
