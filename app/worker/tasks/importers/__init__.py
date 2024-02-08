"""
Module for csv file importers to be sent to queue
"""
from celery import shared_task

from app.worker.app_celery import AppTask

from .historical_data_importer import HistoricalDataImporter


@shared_task(bind=True, base=AppTask)
def historical_data_importer(self, csvpath):
    importer = HistoricalDataImporter(csvpath)
    importer()
