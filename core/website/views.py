from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ContactSerializer, NewsLetterSerializer
# Create your views here.


class ContactView(APIView):

    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Your ticket has been sent successfully"}, status=status.HTTP_200_OK)


class NewsLetterView(APIView):

    def post(self, request):
        serializer = NewsLetterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Now you can find news on your email"}, status=status.HTTP_200_OK)