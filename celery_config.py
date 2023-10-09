from celery import Celery
import os
from dcrm.settings import CELERY_BROKER_URL
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dcrm.settings")
app = Celery('dcrm')
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.broker_url = CELERY_BROKER_URL

app.autodiscover_tasks()


@app.task
def sum():
    time.sleep(2)
    print(2+3)