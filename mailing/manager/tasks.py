from celery.app import shared_task
from celery_singleton import Singleton
from django.db.models.query_utils import Q
import requests

from manager.models import Message


@shared_task(base=Singleton)
def send_mailing(mailing_id):
    from manager.models import Client, Mailing

    mailing = Mailing.objects.only("filter").get(pk=mailing_id)
    clients_to_send = Client.objects.filter(
        Q(operator_code=mailing.filter) | Q(tag=mailing.filter)
    )

    for client in clients_to_send[0:2]:
        payload = {
            "id": 1,
            "phone": int(client.phone_number),
            "text": mailing.text,
        }

        response = requests.post(
            "https://probe.fbrq.cloud/v1/send/1",
            data=payload,
            headers={
                "Authorization": f"Bearer {TOKEN}",
                "Content-Type": "application/json",
            },
        )

        Message.objects.create(
            status=response.status_code, mailing=mailing, client=client
        )
