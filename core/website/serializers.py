from rest_framework import serializers
from .models import TicketModel, NewsLetterModel

class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = TicketModel
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
