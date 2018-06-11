from celery import current_task, shared_task
from dateutil.parser import parse
from django.http import HttpResponse
import csv
import re

from app.models import Item, Donor, Donation

# FIELD_NAMES = [
#     "TR#",
#     "Date",
#     "Donor Name",
#     "Address",
#     "Unit",
#     "City",
#     "Prov.",
#     "Postal Code",
#     "Contact",
#     "Telephone",
#     "Mobile",
#     "PPC",
#     "TRV",
#     "Email",
#     "Qty",
#     "Manufacturer",
#     "Model",
#     "Item Description",
#     "Item Particulars",
#     "Working",
#     "Condition",
#     "Quality",
#     "Batch",
#     "Value",
#     "CustRef"]

FIELD_NAMES = ["first_name", "last_name"]

@shared_task
def exporter():
    global FIELD_NAMES
    response = HttpResponse(content_type="application/csv")
    response["Content-Disposition"] = "attachment; filename='somefilename.csv'"

    writer = csv.DictWriter(response, fieldnames=FIELD_NAMES)
    writer.writeheader()

    writer.writerow({"first_name": "Baked", "last_name": "Beans"})
    writer.writerow({"first_name": "Lovely", "last_name": "Spam"})
    writer.writerow({"first_name": "Wonderful", "last_name": "Spam"})

    return response



"""
Private Methods
"""


def export_row(item):
    try:
        row = {k: unicode(v, "utf-8", errors="ignore").strip()
               for k, v in row.items()}

        donor_obj = get_or_create_donor(parse_donor(row))
        donation_obj = get_or_create_donation(donor_obj, parse_donation(row))
        return new_item(donation_obj, parse_item(row))
    except BaseException:
        print "Problematic Row:"
        print row
        raise


def update_state(percent):
    current_task.update_state(
        state="PROGRESS",
        meta={
            "state": "PROGRESS",
            "process_percent": percent
        }
    )
