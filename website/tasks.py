from celery import shared_task
from .views import update_record
from celery_singleton import Singleton
import time

@shared_task(base=Singleton)
def update_record_task(request, pk):
    ...
