"""
Module for csv file importers to be sent to queue
"""
from celery import task

from .historical_data_importer import HistoricalDataImporter


@task
def historical_data_importer(csvpath):
    importer = HistoricalDataImporter(csvpath)
    importer()
