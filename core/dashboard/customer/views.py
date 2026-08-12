from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import ProfileSerializer
from ..permissions import HasCustomerPermission


class CustomerProfileView(APIView):

    permission_classes = [HasCustomerPermission]

    def get(self, request):
        profile = request.user.user_profile
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def patch(self, request):
        serializer = ProfileSerializer(
            data=request.data,
            instance = request.user.user_profile,
            partial=True
            )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message":"Profile Information Updated",
            "data":serializer.data}, status=status.HTTP_200_OK)