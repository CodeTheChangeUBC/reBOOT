from __future__ import absolute_import
import os
from celery import Celery

from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reboot.settings')
app = Celery('reboot', backend='amqp', broker='amqp://guest@localhost//')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(
    BROKER_URL='amqp://guest@localhost//',
    CELERY_RESULT_BACKEND='amqp://guest@localhost//',
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
)


'''
#FOR CELERY
import djcelery
djcelery.setup_loader()
BROKER_URL = 'amqp://guest@localhost//'
CELERY_RESULT_BACKEND = 'amqp://guest@localhost//'
BROKER_TRANSPORT_OPTIONS = {'confirm_publish': True}
CELERY_RESULT_SERIALIZER = 'json'
CELERY_IGNORE_RESULT = False # this is less important
CELERY_SEND_TASK_SENT_EVENT = True
CELERY_TRACK_STARTED = True
'''
