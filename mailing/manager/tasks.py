from celery.app import shared_task
from celery_singleton import Singleton
from django.db.models.query_utils import Q



@shared_task(base=Singleton)
def send_mailing(mailing_id):
    from manager.models import Client, Mailing

    mailing_filter = Mailing.objects.only("filter").get(pk=mailing_id).filter
    print(mailing_filter)
    clients_to_send = Client.objects.filter(
        Q(operator_code=mailing_filter) | Q(tag=mailing_filter)
    )
    print(clients_to_send)
