"""
Module for csv file importers to be sent to queue
"""
# from celery import task

from app.worker.app_celery import AppTask
from reboot.celery import app

from .historical_data_importer import HistoricalDataImporter


@app.task(bind=True, base=AppTask)
def historical_data_importer(self, csvpath):
    importer = HistoricalDataImporter(csvpath)
    importer()
