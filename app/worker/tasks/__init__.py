'''
Module for tasks to be sent on task queue
'''
from celery import task

from app.worker.app_celery import AppTask
from .create_receipt import Receiptor


@task(bind=True, base=AppTask)
def receiptor(self, queryset, total_count):
    receiptor = Receiptor(queryset, total_count)
    return receiptor()
