from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User


class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"Detail":"Password didn`t match"})
        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"Detail":[e.messages]})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(
            email = validated_data["email"],
            password = validated_data["password"]
        )
        return user


class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        validated_data["email"] = self.user.email
        return validated_data