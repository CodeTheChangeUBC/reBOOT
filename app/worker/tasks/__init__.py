'''
Module for tasks to be sent on task queue
'''
from app.worker.app_celery import AppTask
# from celery import task
from reboot.celery import app

from .create_receipt import Receiptor


@app.task(bind=True, base=AppTask)
def receiptor(self, queryset, total_count):
    receiptor = Receiptor(queryset, total_count)
    return receiptor()
