from rest_framework import serializers
from manager.models import Mailing, Client, Message


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "phone_number", "tag", "timezone"]


class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = ["id", "start_date", "stop_date", "text", "filter"]


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "start_date", "status", "mailing", "client"]
