from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
import secrets
from django.utils import timezone
from datetime import timedelta

from .serializers import (RegistrationSerializer, 
                        LoginSerializer, 
                        ChangePasswordSerializer, 
                        PasswordResetSerializer, 
                        PasswordResetVerifySerializer,
                        )
from .models import User, OtpTokenModel
# Create your views here.


class RegistrationView(APIView):

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Account created successfully"}, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class ChangePasswordView(APIView):

    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        if not user.check_password(serializer.validated_data["old_password"]):
            return Response({"message":"Old Password is wrong"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return Response({"message":"Password changed successfully"})



class PasswordResetView(APIView):


    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        user = User.objects.filter(email=email).first()

        if not user:
            return Response({"message":"This email not excist"}, status=status.HTTP_404_NOT_FOUND)

        otp_password = ''.join(secrets.choice("0123456789") for i in range(8))
        created_date = timezone.now()

        otp_token = OtpTokenModel.objects.create(otp=otp_password, 
                                                user=user,
                                                expired_date=created_date+timedelta(minutes=2))

        send_mail(
            subject="This is you`r OTP code",
            message=f"Your OTP code for resetting your password is: {otp_password}\nThis code will expire in 2 minutes.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )

        return Response({"message":"Code sent to your email"}, status=status.HTTP_200_OK)



class PasswordResetVerifyView(APIView):

    def post(self, request):
        serializer = PasswordResetVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        otp_code = serializer.validated_data["otp_code"]

        user = get_object_or_404(User, email=email)

        try:
            otp = OtpTokenModel.objects.get(user=user, otp=otp_code)
        except OtpTokenModel.DoesNotExist:
            return Response({"message":"This Token is invalid"}, status=status.HTTP_400_BAD_REQUEST)

        if otp.expired_date <= timezone.now():
            return Response({"message":"Token Expired"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message":"Toekn is Valid"}, status=status.HTTP_200_OK)


            
        

        