import csv
from celery import task
from dateutil.parser import parse
from django.utils import timezone

from app.constants.item_map import ITEM_MAP
from app.models import Donor, Donation, Item, ItemDevice, ItemDeviceType
from app.worker.app_celery import set_complete, update_percent


@task
def historical_importer(csvfile):
    '''
    Takes 10b format file path and imports into the database using the 10x
    format into the appropriate tables

    :param str csvfile: csvfile path
    '''
    item_bulk = []
    row_count, prev_percent = 0, 0

    try:
        read_file = csv.DictReader(csvfile, delimiter=',')
        row_total = sum(1 for line in csv.DictReader(csvfile))
        update_percent(0)
        for row in read_file:
            row = _safe_row(row)
            donor = _goc_donor(_parse_donor(row))
            donation = _goc_donation(_parse_donation(row), donor)
            device_type = _goc_device_type(_parse_device_type(row))
            device = _goc_item_device(_parse_item_device(row), device_type)
            item_bulk.append(_new_item(_parse_item(row), donation, device))
            row_count += 1
            prev_percent = _log_status_if_update(
                row_count, row_total, prev_percent)
        print("Adding all items")
        Item.objects.bulk_create(item_bulk)
        print("Import Completed")
    except Exception as e:
        print('Error on row #%s' % row_count)
        print(e)
    set_complete()


def _parse_date(date_f):
    date = parse(date_f, dayfirst=True)
    return date.strftime('%Y-%m-%d')


def _parse_donor(row):
    '''
    Takes a csv row and parses relevant data into a dict

    :param dict row: A CSV row dict
    :return: Donor related data dict
    :rtype: dict
    '''
    receipt_option_f = {
        'Not Needed': 'REFUSED',
        'E-Mail': 'EMAIL',
        'Mail': 'MAIL'
    }[row['TRV']]
    documented_at_f = _parse_date(row['Date'])
    tele_no_f = row['Telephone'] if row['Telephone'] != 'xxxxxxxx' else ''

    return {
        'donor_name': row['Donor Name'],
        'contact_name': row['Contact'],
        'email': row['Email'],
        'want_receipt': receipt_option_f,
        'telephone_number': tele_no_f,
        'mobile_number': row['Mobile'],
        'address_line_one': row['Address'],
        'address_line_two': row['Unit'],
        'city': row['City'],
        'province': row['Prov.'],
        'postal_code': row['Postal Code'][:7],
        'customer_ref': row['CustRef'],
        'documented_at': documented_at_f
    }


def _parse_donation(row):
    '''
    Takes a csv row and parses relevant data into a dict

    :param dict row: A CSV row dict
    :return: Donation related data dict
    :rtype: dict
    '''
    donate_date_f = _parse_date(row['Date'])
    documented_at_f = _parse_date(row['Date'])

    return {
        'tax_receipt_no': row['TR#'],
        'donate_date': donate_date_f,
        'pledge_date': donate_date_f,
        'pick_up': row['PPC'],
        'source': 'HISTORICAL_DATA', # Fixed
        'documented_at': documented_at_f,
        'tax_receipt_created_at': timezone.now()
    }


def _parse_device_type(row):
    '''
    Takes a csv row and parses relevant data into a dict

    :param dict row: A CSV row dict
    :return: ItemDeviceType related data dict
    :rtype: dict
    '''
    return ITEM_MAP[row['Item Description'].lower()]


def _parse_item_device(row):
    '''
    Takes a csv row and parses relevant data into a dict

    :param dict row: A CSV row dict
    :return: ItemDevice related data dict
    :rtype: dict
    '''
    return {
        'make': row['Manufacturer'],
        'model': row['Model'],
        'cpu_type': '',
        'speed': '',
        'memory': None,
        'hd_size': None,
        'screen_size': '',
        'hdd_serial_number': '',
        'operating_system': ''
    }

def _parse_item(row):
    '''
    Takes a csv row and parses relevant data into a dict

    :param dict row: A CSV row dict
    :return: Item related data dict
    :rtype: dict
    '''
    working_f = row['Working'].lower() == 'y'
    value_f = 0 if not row['Value'] else row['Value']
    documented_at_f = _parse_date(row['Date'])
    batch_f = '' if row['Batch'] == '0' else row['Batch']

    return {
        'serial_number': '',
        'asset_tag': '',
        'particulars': row['Item Particulars'],
        'quantity': row['Qty'],
        'working': working_f,
        'condition': row['Condition'],
        'quality': row['Quality'],
        'batch': batch_f,
        'value': value_f,
        'verified': True,
        'documented_at': documented_at_f,
        'notes': ''
        # 'status':
        # 'weight':
        # 'valuation_date':
        # 'valuation_supporting_doc':
    }


def _goc_donor(data):
    '''
    get_or_create a Donor

    :param dict row: A Donor dict
    :return: Donor object
    :rtype: app.models.Donor instance
    '''
    donor, unique = Donor.objects.get_or_create(**data)
    return donor


def _goc_donation(data, donor):
    '''
    get_or_create a Donation

    :param dict row: A Donation dict
    :param obj donor: app.model.Donor object
    :return: Donation object
    :rtype: app.models.Donation instance
    '''
    try:
        d = Donation.objects.get(tax_receipt_no=data.get('tax_receipt_no'))
    except Exception:
        d = Donation.objects.create(donor=donor, **data)
    return d

def _goc_device_type(data):
    '''
    get_or_create a ItemDeviceType

    :param dict row: A ItemDeviceType dict
    :return: ItemDeviceType object
    :rtype: app.models.ItemDeviceType instance
    '''
    dtype, unique = ItemDeviceType.objects.get_or_create(**data)
    return dtype

def _goc_item_device(data, dtype):
    '''
    get_or_create a ItemDevice

    :param dict row: A ItemDevice dict
    :param obj device_type: app.model.ItemDeviceType object
    :return: ItemDevice object
    :rtype: app.models.ItemDevice instance
    '''
    try:
        i = ItemDevice.objects.get(**data)
    except Exception:
        i = ItemDevice.objects.create(dtype=dtype, **data)
    return i

def _new_item(data, donation, device):
    '''
    Initialize a new Item object

    :param dict row: A Item dict
    :param obj donation: app.model.Donation object
    :param obj device: app.model.ItemDevice object
    :return: Item object
    :rtype: app.models.Item instance
    '''
    return Item(donation=donation, device=device, **data)

def _safe_row(row):
    '''
    Takes a row in a csv file row dict and strips spaces into removing
    trivial cases

    :param dict row: A csv file row dict
    '''
    return {k: v.strip() for k, v in list(row.items())}


def _log_status_if_update(count, total, prev):
    '''
    Takes current row count, total count, and previous percentage and logs
    if there is a difference.

    :param int count: The current count of rows parsed
    :param int total: The total count of rows
    :param int prev: The previous percentage parsed
    :return: The current percentage parsed
    :rtype: int
    '''
    new = int(100 * float(count) / float(total))
    if new != prev:
        update_percent(new)
        print("Processed row #%s ||| %s%%" % (count, new))
    return new
