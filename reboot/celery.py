import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reboot.settings')

app = Celery('reboot')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('reboot.celeryconfig')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
