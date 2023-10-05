from app.utils.stripped_csv_reader import StrippedDictReader
from app.worker.app_celery import set_success, update_percent
from app.worker.tasks.logger_task import LoggerTask


class BaseCsvImporter(LoggerTask):
    """ BaseCsvImporter for templating other CSV file related import to the app
    """
    bulk_model = None   # Bulk model type
    model_bulk = None   # Array of bulk_model objects to be saved
    csvpath = None      # CSV file path
    current_pct, current_row, total_rows = 0, 0, 0

    def __init__(self, csvpath):
        self.csvpath = csvpath
        if self.bulk_model is not None:
            self.model_bulk = []
        super().__init__()

    def __call__(self):
        try:
            rows = StrippedDictReader(self.csvpath, delimiter=',')
            print(rows.fieldnames)
            self.total_rows = sum(1 for line in rows)
            self.csvpath.seek(0)
            rows = StrippedDictReader(self.csvpath, delimiter=',')
            update_percent(0)

            self.parse_rows(rows)
            self.logger.info("Parsed all rows")
            if self.bulk_model is not None:
                self.create_bulk_model()
                self.logger.info(f"Bulk created {len(self.model_bulk)} rows")

            set_success()
            self.logger.info("Import completed")
        except Exception as e:
            self.logger.error(f"Error on row #{self.current_row}")
            raise e

    def parse_rows(self, rows):
        """ Iterates over rows in a CSV file and runs parse_row on each row
        """
        try:
            for row in rows:
                row = self._safe_row(row)
                self.parse_row(row)
                self.current_row += 1
                self._log_status_if_pct_update()
        except Exception as e:
            self.logger.error(f"Row Data: {row}")
            raise e

    def parse_row(self):
        """ Parses a CSV row into related models and create them as needed.
        Adds to model_bulk if there is a bulk_model. Must be overwritten
        """
        raise NotImplementedError

    def create_bulk_model(self):
        """ Bulk creates the bulk_model
        """
        return self.bulk_model.objects.bulk_create(self.model_bulk)

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
    def _safe_row(row):
        """ Takes a row in a csv file row dict and strips spaces

        :param dict row: A csv file row dict
        """
        return {k: v.strip() for k, v in list(row.items())}
