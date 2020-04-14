import csv
from celery import task
from django.http import HttpResponse

from app.constants.field_names import CURRENT_FIELDS
from app.models import Item
from app.worker.app_celery import AppTask, update_percent


@task(bind=True, base=AppTask)
def exporter(self, file_name):
    update_percent(0)

    response = HttpResponse(content_type="application/csv")
    response["Content-Disposition"] = f"attachment;filename={file_name}.csv"
    writer = csv.DictWriter(response, fieldnames=CURRENT_FIELDS)
    writer.writeheader()

    previous_percent, cur_count = 0, 0
    total_count = Item.objects.count()

    for item in Item.objects.all():
        writer.writerow(format_row(item))
        cur_count += 1
        process_percent = int(100 * float(cur_count) / float(total_count))
        if process_percent != previous_percent:
            update_percent(process_percent)
            previous_percent = process_percent
            print(f"Exported row #{cur_count} ||| {process_percent}%")
    print('Exporting completed')
    return response


"""
Private Methods
"""


def format_row(item):
    try:
        row = merge_dict({}, item.device.csv_dict())
        row = merge_dict(row, item.csv_dict())
        row = merge_dict(row, item.donation.csv_dict())
        row = merge_dict(row, item.donation.donor.csv_dict())
        return row
    except BaseException:
        print("Problematic row:")
        print("Item:", item.id)
        print("Donation:", item.donation.tax_receipt_no)
        print("Donor:", item.donation.donor.id)
        raise


def merge_dict(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z
