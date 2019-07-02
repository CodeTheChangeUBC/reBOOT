from celery import current_task, task
from celery.states import SUCCESS
from django.http import HttpResponse
import csv

from app.models import Item, Donor, Donation


@task
def exporter(file_name):
    result = {
        "file_name": file_name,
        "rows": []
    }
    rows = []
    previous_percent, current_count = 0, 0
    total_count = Item.objects.count()
    items = Item.objects.all()
    for item in items:
        rows.append(export_row(item))
        current_count += 1
        process_percent = int(100 * float(current_count) / float(total_count))
        if process_percent != previous_percent:
            update_state(process_percent)
            previous_percent = process_percent

    result["rows"] = rows
    current_task.update_state(state=SUCCESS, meta={
        "state": SUCCESS,
        "process_percent": 100
    })
    return result


"""
Private Methods
"""


def update_state(percent):
    current_task.update_state(
        state="PROGRESS",
        meta={
            "state": "PROGRESS",
            "process_percent": percent
        }
    )


def export_row(item):
    try:
        row = merge_dict({}, item_data(item))
        row = merge_dict(row, donation_data(item.donation))
        row = merge_dict(row, donor_data(item.donation.donor))
        return row
    except BaseException:
        print("Problematic row:")
        print("Item:" + item.id)
        print("Donation:" + item.donation.tax_receipt_no)
        print("Donor:" + item.donation.donor.id)
        raise


def item_data(item):
    return {
        "Item Description": item.description,
        "Item Particulars": item.particulars,
        "Manufacturer": item.manufacturer,
        "Qty": item.quantity,
        "Model": item.model,
        "Working": "true" if item.working else "false",
        "Condition": item.condition,
        "Quality": item.quality,
        "Batch": item.batch,
        "Value": item.value,
        "Status": item.status
    }


def donation_data(donation):
    return {
        "TR#": donation.tax_receipt_no,
        "Date": donation.donate_date,
        "PPC": donation.pick_up,
        "TRV": None,
    }


def donor_data(donor):
    return {
        "Donor Name": donor.donor_name,
        "Email": donor.email,
        "Telephone": donor.telephone_number,
        "Mobile": donor.mobile_number,
        "Address": donor.address_line,
        "City": donor.city,
        "Postal Code": donor.postal_code,
        "CustRef": donor.customer_ref
    }


def merge_dict(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z
