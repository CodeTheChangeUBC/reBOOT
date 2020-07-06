"""
Module for csv file importers to be sent to queue
"""
from celery import task

from app.worker.app_celery import AppTask
from .historical_data_importer import HistoricalDataImporter
from .webform_data_importer import WebformDataImporter


@task(bind=True, base=AppTask)
def historical_data_importer(self, csvpath):
    importer = HistoricalDataImporter(csvpath)
    importer()


@task(bind=True, base=AppTask)
def webform_data_importer(self, csvpath):
    importer = WebformDataImporter(csvpath)
    importer()
