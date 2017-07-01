from celery.utils.log import get_task_logger
from celery import shared_task
from .models import Alerts

logger = get_task_logger(__name__)


@shared_task
def create_alert_task():

    new_alert = Alerts.objects.create(
        message='A bill was created!',
    )

    new_alert.save()

    return new_alert
