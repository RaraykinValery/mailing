from django.db.models import Count
from django.db.models.expressions import Case, When
from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from manager.models import Mailing, Client, Message
from manager.serializers import MailingSerializer, ClientSerializer, MessageSerializer


def auth(request):
    return render(request, "oauth.html")


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]


class MailingViewSet(viewsets.ModelViewSet):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer
    permission_classes = [IsAuthenticated]


class MailingGeneralStatistics(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        now = timezone.now()
        mailings_numbers_grouped_by_status = (
            Mailing.objects.all().aggregate(
                complited=Count(Case(When(stop_date__lt=now, then=1))),
                active=Count(
                    Case(When(stop_date__gt=now, start_date__lt=now, then=1))),
                waiting=Count(Case(When(start_date__gt=now, then=1))),
            ),
        )
        messages_numbers_grouped_by_status = Message.objects.values("status").annotate(
            messages_count=Count("id")
        )
        data = {
            "mailings": mailings_numbers_grouped_by_status,
            "messages": messages_numbers_grouped_by_status,
        }
        return Response(data)


class MailingDetailStatistics(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        mailing_messages = Message.objects.filter(mailing=pk)
        serializer = MessageSerializer(mailing_messages, many=True)
        return Response(serializer.data)
