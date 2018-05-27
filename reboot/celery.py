from __future__ import absolute_import
from celery import Celery
from django.conf import settings
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reboot.settings')

app = Celery('reboot', backend=settings.CELERY_BACKEND_TYPE)

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.conf.update(
    BROKER_URL=settings.CELERY_BROKER_URL,
    CELERY_RESULT_BACKEND=settings.CELERY_RESULT_BACKEND,
    task_serializer=settings.CELERY_TASK_SERIALIZER,
    CELERY_ACCEPT_CONTENT=settings.CELERY_ACCEPT_CONTENT,
    result_serializer=settings.CELERY_RESULT_SERIALIZER,
)

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)