from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import RegistrationSerializer
# Create your views here.


class RegistrationView(APIView):

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"Detail":"Account created successfully"}, status=status.HTTP_201_CREATED)
    
