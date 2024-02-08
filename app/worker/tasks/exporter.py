import csv

from celery import shared_task
from celery.utils.log import get_task_logger
from django.core import serializers
from django.db.models.query import QuerySet
from django.http import HttpResponse

from app.constants.field_names import CURRENT_FIELDS
from app.worker.app_celery import AppTask, update_percent


@shared_task(bind=True, base=AppTask)
def exporter(self, file_name, qs: QuerySet = None, total_count: int = 0):
    rows = serializers.deserialize('json', qs)
    csv_exporter = CsvExporter(file_name, rows, total_count)
    return csv_exporter()


class CsvExporter:
    """CsvExporter for exporting to 10x format"""
    logger = None
    file_name = ""
    current_pct, current_row, total_rows = 0, 0, 0

    def __init__(self, file_name, rows: QuerySet, total_count: int):
        self.total_rows = total_count
        self.file_name = file_name
        if self.logger is None:
            self.logger = get_task_logger(__name__)
        self.rows = rows

    def __call__(self):
        try:
            update_percent(0)
            output = CsvExporter.create_csv_response(self.file_name)
            writer = csv.DictWriter(output, fieldnames=CURRENT_FIELDS)
            writer.writeheader()

            for row in self.rows:
                item = row.object
                writer.writerow(self.format_row(item))
                self.current_row += 1
                self._log_status_if_pct_update()

            self.logger.info("Export completed")
            return output  # Celery will set SUCCESS on return
        except Exception:
            self.logger.error(f"Error on row #{self.current_row}")
            raise

    def format_row(self, item):
        try:
            row = merge_dict({}, item.device.csv_dict())
            row = merge_dict(row, item.csv_dict())
            row = merge_dict(row, item.donation.csv_dict())
            row = merge_dict(row, item.donation.donor.csv_dict())
            return row
        except Exception:
            self.logger.error(
                f"Error row: {item}, {item.donation}, {item.donation.donor}")
            raise

    def _log_status_if_pct_update(self):
        """ Calculates new counts and percentages and logs if diff pct
        """
        new_pct = int(100 * float(self.current_row) / float(self.total_rows))
        if new_pct != self.current_pct:
            self.current_pct = new_pct
            update_percent(new_pct)
            self.logger.info(
                f"Processed row #{self.current_row} ||| {new_pct}%")

    @staticmethod
    def create_csv_response(file_name):
        res = HttpResponse(content_type="application/csv")
        res["Content-Disposition"] = f"attachment;filename={file_name}.csv"
        return res


"""
Private Methods
"""


def merge_dict(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z
