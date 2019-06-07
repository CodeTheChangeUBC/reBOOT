from __future__ import absolute_import
from celery import Celery
from django.conf import settings
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reboot.settings')

app = Celery(
    'reboot',
    broker=settings.CELERY_BROKER_URL,
    task_serializer=settings.CELERY_TASK_SERIALIZER,
    accept_content=settings.CELERY_ACCEPT_CONTENT,
    result_serializer=settings.CELERY_RESULT_SERIALIZER
)

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
