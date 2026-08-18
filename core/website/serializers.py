from rest_framework import serializers
from .models import ContactModel, NewsLetterModel

class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactModel
        fields = [
            "first_name",
            "last_name",
            "phone_number",
            "message"
        ]


class NewsLetterSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewsLetterModel
        fields = [
            "email"
        ]
