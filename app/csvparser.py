import csv
from .models import Donor
from .models import Donation
from .models import Item

def parser(csvfile):
    read_file = csv.reader(csvfile, delimiter = ',')
    rowcount = 0
    #Testing
    listofnames = []
    for row in read_file:
        if(rowcount != 0):


            date = row[0]
            business_name = row[2]
            first_name = row[3]
            last_name = row[4]
            address = row[5]
            address2 = row[6]
            email = row[7]

            rowcount += 1



