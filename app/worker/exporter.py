import csv
from celery import current_task, task
from celery.states import SUCCESS
from django.http import HttpResponse

from app.constants.field_names import FIELD_NAMES
from app.models import Item, Donor, Donation


@task
def exporter(file_name):
    response = HttpResponse(content_type="application/csv")
    response["Content-Disposition"] = "attachment;" + \
        "filename=" + file_name + ".csv"
    writer = csv.DictWriter(response, fieldnames=FIELD_NAMES)
    writer.writeheader()

    previous_percent, cur_count = 0, 0
    total_count = Item.objects.count()
    items = Item.objects.all()
    update_state(0)

    for item in items:
        writer.writerow(export_row(item))
        cur_count += 1
        process_percent = int(100 * float(cur_count) / float(total_count))
        if process_percent != previous_percent:
            update_state(process_percent)
            previous_percent = process_percent
            print('Exported row #%s ||| %s%%' % (cur_count, process_percent))

    current_task.update_state(state=SUCCESS, meta={
        "state": SUCCESS,
        "process_percent": 100
    })
    return response


"""
Private Methods
"""


def update_state(percent):
    current_task.update_state(state="PROGRESS", meta={
        "state": "PROGRESS",
        "process_percent": percent
    })


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
