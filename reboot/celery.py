from celery import Celery
from django.conf import settings
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reboot.settings')

app = Celery()
app.config_from_object('reboot.celeryconfig')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
