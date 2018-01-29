'''
Module for tasks to be sent on task queue 
'''
from celery.decorators import task
from celery import Celery, current_task, shared_task
import csv
import datetime
import zipfile
from .models import Donor, Donation, Item
# Note for celery:
# This is using RabbitMQ. To run, must have a worker running the tasks
# Use 'celery -A reboot worker -l info'
# Then in another terminal, run 'python manage.py runserver'
# Make sure worker is running, then tassk will be queued by worker to parse the data.


@shared_task
def parser(csvfile):
    item_bulk = []
    '''
	Helper Function
	Checks for existing donor matching the given parameter:
	- if exists, return donor_id
	- else, create new Donor object and return its donor_id
	'''
    def getCreateDonor(donor_name_f, email_f, want_receipt_f, telephone_number_f, telephone_extension_f, mobile_number_f, mobile_extension_f, address_line_f, city_f, province_f, postal_code_f, customer_ref_f):

        want_receipt_f = "email" in want_receipt_f.lower() or "e-mail" in want_receipt_f.lower()

        result_donor, unique = Donor.objects.get_or_create(donor_name=donor_name_f, email=email_f, want_receipt=want_receipt_f, telephone_number=telephone_number_f, telephone_extension=telephone_extension_f,
                                                           mobile_number=mobile_number_f, mobile_extension=mobile_extension_f, address_line=address_line_f, city=city_f, province=province_f,
                                                           postal_code=postal_code_f, customer_ref=customer_ref_f, verified=True)
        return result_donor

    '''
	Helper Function
	Checks for existing donation matching the given parameter:
	- if exists, return donation_id/tax_receipt_no
	- else, create new Donation object and return its donation_id/tax_receipt_no
	'''
    def addCreateDonation(donor_f, tax_receipt_no_f, donate_date_f, pick_up_f):
        donate_date_f = parseDate(donate_date_f)
        result_donation = None
        try:
            result_donation = Donation.objects.get(tax_receipt_no=tax_receipt_no_f)
        except Donation.DoesNotExist:
            result_donation = Donation.objects.create(donor_id=donor_f, tax_receipt_no=tax_receipt_no_f, donate_date=donate_date_f, verified=True, pick_up=pick_up_f)
        return result_donation

    '''
	Helper Function
	Insert new Item using the parameters
	Returns nothing
	'''
    def addItem(donation_f, description_f, particulars_f, manufacturer_f, model_f, quantity_f, working_f, condition_f, quality_f, batch_f, value_f):
        working_f = working_f == "Y"
        value_f = 0 if not value_f else value_f
        item_bulk.append(Item(tax_receipt_no=donation_f, description=description_f, particulars=particulars_f, manufacturer=manufacturer_f, model=model_f,
                              quantity=quantity_f, working=working_f, condition=condition_f, quality=quality_f, batch=batch_f, value=value_f, verified=True))

    def getTeleExt(telephone):
        if "xxxxxx" not in telephone:
            teleNo = telephone_number_All.partition(" ext.")[0]
            teleExt = telephone_number_All.partition(" ext.")[2]
        else:
            teleNo = ""
            teleExt = ""
        return [teleNo, teleExt]


    def getMobileExt(mobile):
        if "xxxxxx" not in mobile:
            mobNo = mobile_number_All.partition(" ext.")[0]
            mobExt = mobile_number_All.partition(" ext.")[2]
        else:
            mobNo  = ""
            mobExt =  ""
        return [mobNo, mobExt]


    '''
	Helper Function
	Takes verbose date
	Returns string
	'''
    def parseDate(date_f):
        date_f = date_f.split(", ")[1]
        date_f = date_f.split(" ")

        months = {"January": "01", "February": "02", "March": "03", "April": "04",
                    "May": "05", "June": "06", "July": "07", "August": "08",
                    "September": "09", "October": "10", "November": "11", "December": "12"}

        result = date_f[2] + "-" + months.get(date_f[1]) + "-" + date_f[0]
        return result

    # Use the 10b dummy.csv
    read_file = csv.reader(csvfile, delimiter=',')[1:]
    # fileObject is your csv.reader
    total_row_count = sum(1 for line in csv.reader(csvfile)[1:])
    previous_percent = 0

    for row in read_file:
        process_percent = int(100 * float(row_count) / float(total_row_count))
        if process_percent != previous_percent:
            current_task.update_state(state='PROGRESS', meta={'process_percent': process_percent})
            previous_percent = process_percent

        tax_receipt_no_f    = unicode(row[1],  "utf-8", errors='ignore')

        donate_date_f       = unicode(row[3],  "utf-8", errors='ignore')
        donor_name_f        = unicode(row[4],  "utf-8", errors='ignore')
        address_line_f      = unicode(row[5],  "utf-8", errors='ignore')

        city_f              = unicode(row[7],  "utf-8", errors='ignore')
        province_f          = unicode(row[8],  "utf-8", errors='ignore')
        postal_code_f       = unicode(row[9],  "utf-8", errors='ignore')

        telephone           = unicode(row[11],  "utf-8", errors='ignore')
        mobile              = unicode(row[12],  "utf-8", errors='ignore')



        pick_up_f           = unicode(row[13], "utf-8", errors='ignore')
        want_receipt_f      = unicode(row[14], "utf-8", errors='ignore')
        email_f             = unicode(row[15], "utf-8", errors='ignore')
        quantity_f          = unicode(row[16], "utf-8", errors='ignore')
        manufacturer_f      = unicode(row[17], "utf-8", errors='ignore')
        model_f             = unicode(row[20], "utf-8", errors='ignore')
        description_f       = unicode(row[21], "utf-8", errors='ignore')
        particulars_f       = unicode(row[22], "utf-8", errors='ignore')
        working_f           = unicode(row[23], "utf-8", errors='ignore')
        condition_f         = unicode(row[24], "utf-8", errors='ignore')
        quality_f           = unicode(row[25], "utf-8", errors='ignore')
        batch_f             = unicode(row[26], "utf-8", errors='ignore')
        value_f             = unicode(row[27], "utf-8", errors='ignore')
        customer_ref_f      = unicode(row[28], "utf-8", errors='ignore')

        teleValue = getTeleExt(telephone)
        mobileValue = getMobileExt(mobile)

        donor_f = getCreateDonor(donor_name_f, email_f, want_receipt_f, teleValue[0],teleValue[1],
                                    mobileValue[0], mobileValue[1], address_line_f, city_f, province_f, postal_code_f, customer_ref_f)
        donation_f = addCreateDonation(donor_f, tax_receipt_no_f, donate_date_f, pick_up_f)
        addItem(donation_f, description_f, particulars_f, manufacturer_f, model_f,
                quantity_f, working_f, condition_f, quality_f, batch_f, value_f)

        print("Parsed row #" + str(row_count) + " ||| Percent = " + str(process_percent))
    print "Adding all items"
    list_of_items = Item.objects.bulk_create(item_bulk)
    print "Parsing Completed"
    
