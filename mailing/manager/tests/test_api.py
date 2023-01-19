from datetime import timedelta
import json

from django.urls.base import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.renderers import JSONRenderer

from manager.models import Client, Mailing
from manager.serializers import MailingSerializer


class ClientsApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_user")
        self.client1 = Client.objects.create(
            phone_number="78908991202",
            operator_code="890",
            tag="vip",
            timezone="Europe/Moscow",
        )
        self.client2 = Client.objects.create(
            phone_number="78918991202",
            operator_code="891",
            tag="vip",
            timezone="Europe/Moscow",
        )

    def test_create(self):
        url = reverse("client-list")
        data = {
            "phone_number": "78998991202",
            "operator_code": "899",
            "tag": "vip",
            "timezone": "Europe/Moscow",
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(
            url, data=json_data, content_type="application/json"
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, Client.objects.count())

    def test_update(self):
        url = reverse("client-detail", args=(self.client1.id,))
        data = {
            "phone_number": self.client1.phone_number,
            "operator_code": self.client1.operator_code,
            "tag": "sop",
            "timezone": self.client1.timezone,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(
            url, data=json_data, content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.client1.refresh_from_db()
        self.assertEqual("sop", self.client1.tag)


class MailingsAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_user")

        self.now = timezone.localtime()
        self.tomorrow = self.now + timedelta(days=1)
        self.yesterday = self.now - timedelta(days=1)

        self.client1 = Client.objects.create(
            phone_number="78908991202",
            tag="friend",
            timezone="Europe/Moscow",
        )
        self.client2 = Client.objects.create(
            phone_number="78918991202",
            tag="vip",
            timezone="Europe/Moscow",
        )
        self.client3 = Client.objects.create(
            phone_number="78988991202",
            tag="friend",
            timezone="Europe/Moscow",
        )

    def test_create(self):
        url = reverse("mailing-list")
        data = {
            "start_date": self.yesterday,
            "stop_date": self.tomorrow,
            "text": "Hello everyone!",
            "filter": "friend",
        }
        serializer = MailingSerializer(data)
        json_data = JSONRenderer().render(serializer.data)

        self.client.force_login(self.user)
        response = self.client.post(
            url, data=json_data, content_type="application/json"
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, Mailing.objects.all().count())
