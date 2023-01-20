import json
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.db.models.query_utils import Q
import pytz
import requests


TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))


class Mailing(models.Model):
    """Сущность рассылка"""

    start_date = models.DateTimeField("Дата начала рассылки")
    stop_date = models.DateTimeField("Дата окончания рассылки")
    text = models.CharField("Текст сообщения", max_length=255)
    filter = models.CharField("Фильтр свойств клиентов", max_length=255)

    def __str__(self):
        return f"Id: {self.id}, text: {self.text}, filter: {self.filter}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        now = timezone.localtime()

        if self.start_date < now and self.stop_date > now:
            clients_to_send = Client.objects.filter(
                Q(operator_code=self.filter) | Q(tag=self.filter)
            )

            for client in clients_to_send:
                data = {
                    "id": 1,
                    "phone": int(client.phone_number),
                    "text": self.text,
                }

                response = requests.post(
                    "https://probe.fbrq.cloud/v1/send/1",
                    data=json.dumps(data),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {TOKEN}",
                    },
                )

                Message.objects.create(
                    status=response.status_code, mailing=self, client=client
                )


class Client(models.Model):
    """Сущность клиент"""

    phone_regex = RegexValidator(
        regex=r"^7\d{10}$",
        message="Phone number must be entered in the format: '79999999999'",
    )
    phone_number = models.CharField(
        "Номер телефона", validators=[phone_regex], max_length=11
    )
    operator_code = models.CharField(
        "Код оператора", max_length=3, editable=False)
    tag = models.CharField("Тэг", max_length=255, blank=True)
    timezone = models.CharField(
        "Часовой пояс", max_length=32, choices=TIMEZONES, default="UTS"
    )

    def __str__(self):
        return f"Id: {self.id}, number: {self.phone_number}, tag: {self.tag}"

    def save(self, *args, **kwargs):
        self.operator_code = self.phone_number[1:4]
        super().save(*args, **kwargs)


class Message(models.Model):
    """Сущность сообщение"""

    start_date = models.DateTimeField(
        "Дата и время создания сообщения", editable=False)
    status = models.IntegerField("Статус отправки")
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, blank=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return (
            f"Mailing {self.mailing.id}, Client {self.client.id}, status {self.status}"
        )

    def save(self, *args, **kwargs):
        self.start_date = timezone.localtime()
        super().save(*args, **kwargs)
