from datetime import timedelta

from django.utils import timezone
from django.test.testcases import TestCase
from manager.models import Client, Mailing, Message

from manager.serializers import ClientSerializer, MailingSerializer, MessageSerializer


class SerialisersTestCase(TestCase):
    def setUp(self):
        self.now = timezone.localtime()
        self.tomorrow = self.now + timedelta(days=1)
        self.yesterday = self.now - timedelta(days=1)
        self.mailing1 = Mailing.objects.create(
            start_date=self.yesterday,
            stop_date=self.tomorrow,
            text="Hello everyone!",
            filter="friend",
        )
        self.client1 = Client.objects.create(
            phone_number="78908991202",
            tag="vip",
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
        self.message1 = Message.objects.create(
            status=200, mailing=self.mailing1, client=self.client1
        )

    def test_client_serializer(self):
        data = ClientSerializer([self.client1, self.client2], many=True).data
        expected_data = [
            {
                "id": self.client1.id,
                "phone_number": "78908991202",
                "tag": "vip",
                "timezone": "Europe/Moscow",
            },
            {
                "id": self.client2.id,
                "phone_number": "78918991202",
                "tag": "vip",
                "timezone": "Europe/Moscow",
            },
        ]
        self.assertEqual(expected_data, data)

    def test_mailing_serializer(self):
        data = MailingSerializer(self.mailing1).data
        expected_data = {
            "id": self.mailing1.id,
            "start_date": self.yesterday.isoformat(),
            "stop_date": self.tomorrow.isoformat(),
            "text": "Hello everyone!",
            "filter": "friend",
        }
        self.assertEqual(expected_data, data)

    def test_message_serializer(self):
        data = MessageSerializer(self.message1).data
        expected_data = {
            "id": self.message1.id,
            "start_date": self.message1.start_date.isoformat(),
            "status": 200,
            "mailing": self.mailing1.id,
            "client": self.client1.id,
        }
        self.assertEqual(expected_data, data)
