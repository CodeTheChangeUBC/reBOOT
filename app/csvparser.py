import csv
from .models import Donor
from .models import Donation
from .models import Item

def parser(csvfile):
    # Use the 10b dummy.csv
    '''
    171108,
    TR#,
    User,
    Date,
    Donor Name,
    Address,
    Unit,
    City,
    Prov.,
    Postal Code,
    Contact,
    Telephone,
    Mobile,
    PPC,
    TRV,
    Email,
    Qty,
    Manufacturer,
    Vmanuf,
    Part No.,
    Model,
    Item Description,
    Item Particulars,
    Working,
    Condition,
    Quality,
    Batch,
    Value,
    CustRef,
    Printer,
    Laptop,
    Computer,
    Monitor,
    Other,
    #REF!,
    #REF!,
    #REF!,
    #REF!,
    #REF!,
    ,
    ,
    ,
    ,
    Printer,
    Laptop,
    Desktop,
    Monitor,
    Other,
    0,
    0,
    0,
    0,
    0,,,
    '''


    read_file = csv.reader(csvfile, delimiter = ',')
    rowcount = 0

    verified = True
    # Donor Variables
    donor_name, email, want_receipt, telephone_number, mobile_number, address_line, city, province, postal_code
    # verified # same for all

    # Donation Variables
    donor_id, tax_receipt_no, donate_date, donor_city
    # verified # same for all

    # Item Variables
    description, manufacturer, model, quantity, working, condition, quality, batch, value
    # verified # same for all
    # tax_receipt_no # pull from donation


    #Testing
    listofnames = []
    for row in read_file:
        if(rowcount != 0):
            donor_name = row[4]
            email = row[15]
            want_receipt = row[14] # use ? : later
            telephone_number = row[11]
            mobile_number = row[12]
            address_line = row[5]
            city = row[7]
            province = row[8]
            postal_code = row[9]
            donor_id = None # Get later
            tax_receipt_no = row[1]
            donate_date = row[3]
            donor_city = row[7]
            description = row[30]
            manufacturer = row[17]
            model = row[20]
            quantity = row[16]
            working = row[23]
            condition = row[24]
            quality = row[25]
            batch = row[26]
            value = row[27]
            donor_id = getDonor(donor_name, email, want_receipt, telephone_number, mobile_number, address_line, city, province, postal_code);
            donation_id = getDonation(donor_id, tax_receipt_no, donate_date, donor_city) # donation_id = tax_receipt_no
            addItem(donation_id, description, manufacturer, model, quantity, working, condition, quality, batch, value)
        rowcount += 1


'''
Checks for existing donor matching the given parameter:
 - if exists, return donor_id
 - else, create new Donor object and return its donor_id
'''
def getDonor(donor_name, email, want_receipt, telephone_number, mobile_number, address_line, city, province, postal_code):
    # TODO:
    result_donor = None
    return result_donor

'''
Checks for existing donation matching the given parameter:
 - if exists, return donation_id/tax_receipt_no
 - else, create new Donation object and return its donation_id/tax_receipt_no
'''
def getDonation(donor, tax_receipt_no, donate_date, donor_city):
    # TODO:
    result_donation = None
    return result_donation

'''
Insert new Item using the parameters
Returns nothing
'''
def addItem(tax_receipt_no, description, manufacturer, model, quantity, working, condition, quality, batch, value):
    # TODO:
    result_item = None
