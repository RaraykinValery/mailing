import os
from datetime import timedelta

from celery import Celery
from django.conf import settings


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mailing.settings")

app = Celery("mailing")
app.config_from_object("django.conf:settings")
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        timedelta(minutes=1),
        get_active_mailings.s(),
        name="debug",
    )


@app.task
def get_active_mailings():
    from manager.models import Mailing
    from django.utils import timezone

    now = timezone.localtime()

    active_mailings = Mailing.objects.filter(
        start_date__lt=now, stop_date__gt=now)
    print(active_mailings)
