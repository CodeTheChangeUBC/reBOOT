import csv
import re
from celery import current_task, shared_task
from celery.states import SUCCESS
from dateutil.parser import parse

from app.models import Item, Donor, Donation


@shared_task
def parser(csvfile):
    item_bulk = []
    row_count, previous_percent = 0, 0
    read_file = csv.DictReader(csvfile, delimiter=',')
    total_row_count = sum(1 for line in csv.DictReader(csvfile))
    update_state(0)
    for row in read_file:
        item_bulk.append(parse_row(row))
        row_count += 1
        process_percent = int(100 * float(row_count) / float(total_row_count))
        if process_percent != previous_percent:
            update_state(process_percent)
            previous_percent = process_percent
            print("Parsed row #%s ||| %s%%" % (row_count, process_percent))
    print("Adding all items")
    Item.objects.bulk_create(item_bulk)
    print("Parsing Completed")
    current_task.update_state(state=SUCCESS, meta={
        "state": SUCCESS,
        "process_percent": 100
    })


'''
Private Methods
'''


def parse_row(row):
    try:
        row = {k: v.strip() for k, v in list(row.items())}

        donor_obj = get_or_create_donor(parse_donor(row))
        donation_obj = get_or_create_donation(donor_obj, parse_donation(row))
        return new_item(donation_obj, parse_item(row))
    except:
        print("Problematic Row:")
        print(row)
        raise


def update_state(percent):
    current_task.update_state(
        state='PROGRESS',
        meta={
            'state': 'PROGRESS',
            'process_percent': percent
        }
    )


def get_or_create_donor(donor_dict):
    ''' Checks for existing donor matching the given parameter:
    If exists, return donor
    Else, create new Donor object and return its donor
    '''
    result_donor, unique = Donor.objects.get_or_create(**donor_dict)
    return result_donor


def get_or_create_donation(donor_obj, donation_dict):
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
            donor=donor_obj,
            **donation_dict
        )
    return result_donation


def new_item(donation_obj, item_dict):
    ''' Return new Item using the parameters
    '''
    return Item(
        donation=donation_obj,
        **item_dict
    )


def parse_date(date_f):
    date = parse(date_f, dayfirst=True)
    return date.strftime('%Y-%m-%d')


def parse_donor(row):
    want_receipt_f = 'email' in re.sub('[^a-z]+', '', row['TRV'].lower())
    documented_at_f = parse_date(row['Date'])
    return {
        'donor_name': row['Donor Name'],
        'email': row['Email'],
        'want_receipt': want_receipt_f,
        'telephone_number': row['Telephone'],
        'mobile_number': row['Mobile'],
        'address_line': row['Address'],
        'city': row['City'],
        'province': row['Prov.'],
        'postal_code': row['Postal Code'][:7],
        'customer_ref': row['CustRef'],
        'verified': True,
        'documented_at': documented_at_f
    }


def parse_donation(row):
    donate_date_f = parse_date(row['Date'])
    documented_at_f = parse_date(row['Date'])
    return {
        'tax_receipt_no': row['TR#'],
        'donate_date': donate_date_f,
        'pick_up': row['PPC'],
        'verified': True,
        'documented_at': documented_at_f
    }


def parse_item(row):
    working_f = row['Working'] == 'Y'
    value_f = 0 if not row['Value'] else row['Value']
    documented_at_f = parse_date(row['Date'])
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
        'documented_at': documented_at_f
    }
