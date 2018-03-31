from celery.decorators import task
from celery import Celery, current_task, shared_task
from app.models import Item, Donor, Donation
import csv
import re
import datetime

@shared_task
def parser(csvfile):
    item_bulk = []
    row_count, previous_percent = 0, 0
    read_file = csv.DictReader(csvfile, delimiter=',')
    total_row_count = sum(1 for line in csv.DictReader(csvfile))

    for row in read_file:
        row = {k: unicode(v, "utf-8", errors='ignore').strip() for k, v in row.items()}

        donor_obj = getCreateDonor(parse_donor(row))
        donation_obj = getCreateDonation(donor_obj, parse_donation(row))
        item_bulk.append(createItem(donation_obj, parse_item(row)))

        row_count += 1
        process_percent = int(100 * float(row_count) / float(total_row_count))
        if process_percent != previous_percent:
            update_state(process_percent)
            previous_percent = process_percent
        print"Parsed row #%s ||| Percent = %s" % (row_count, process_percent)
    print "Adding all items"
    Item.objects.bulk_create(item_bulk)
    print "Parsing Completed"


'''
Private Methods
'''


def update_state(percent):
    current_task.update_state(
        state='PROGRESS',
        meta={
            'state': 'PROGRESS',
            'process_percent': percent
        }
    )


def getCreateDonor(donor_dict):
    ''' Checks for existing donor matching the given parameter:
    If exists, return donor_id
    Else, create new Donor object and return its donor_id
    '''
    result_donor, unique = Donor.objects.get_or_create(**donor_dict)
    return result_donor


def getCreateDonation(donor_obj, donation_dict):
    ''' Checks for existing donation matching the given parameter:
    If exists, return donation_id/tax_receipt_no
    Else, create new Donation object and return its donation_id/tax_receipt_no
    '''
    result_donation = None
    try:
        result_donation = Donation.objects.get(
            tax_receipt_no=donation_dict.get('tax_receipt_no')
        )
    except Donation.DoesNotExist:
        result_donation = Donation.objects.create(
            donor_id=donor_obj,
            **donation_dict
        )
    return result_donation


def createItem(donation_obj, item_dict):
    ''' Return new Item using the parameters
    '''
    return Item(
        tax_receipt_no=donation_obj,
        **item_dict
    )


def parseDate(date_f):
    date_f = date_f.split(", ")[1].split(" ")

    months = {
        "January": "01", "February": "02", "March": "03", "April": "04",
        "May": "05", "June": "06", "July": "07", "August": "08",
        "September": "09", "October": "10", "November": "11", "December": "12"
    }

    result = date_f[2] + "-" + months.get(date_f[1]) + "-" + date_f[0]
    return result


def parse_donor(row):
    want_receipt_f = 'email' in re.sub('[^a-z]+', '', row['TRV'].lower())
    return {
        'donor_name': row['Donor Name'],
        'email': row['Email'],
        'want_receipt': want_receipt_f,
        'telephone_number': row['Telephone'],
        'mobile_number': row['Mobile'],
        'address_line': row['Address'],
        'city': row['City'],
        'province': row['Prov.'],
        'postal_code': row['Postal Code'],
        'customer_ref': row['CustRef'],
        'verified': True
    }


def parse_donation(row):
    donate_date_f = parseDate(row['Date'])
    return {
        'tax_receipt_no': row['TR#'],
        'donate_date': donate_date_f,
        'pick_up': row['PPC'],
        'verified': True
    }


def parse_item(row):
    working_f = row['Working'] == 'Y'
    value_f = 0 if not row['Value'] else row['Value']
    donate_date_f = parseDate(row['Date'])
    return {
        'description': row['Item Description'],
        'particulars': row['Item Particulars'],
        'manufacturer': row['Manufacturer'],
        'model': row['Model'],
        'quantity': row['Qty'],
        'working': working_f,
        'condition': row['Condition'],
        'quality': row['Quality'],
        'batch': row['Batch'],
        'value': value_f,
        'verified': True,
        'created_at_formatted': donate_date_f
    }
