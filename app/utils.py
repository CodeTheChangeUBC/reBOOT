import csv, datetime, zipfile
from io import BytesIO
from xhtml2pdf import pisa
from .models import Donor,Donation,Item
from django.http import HttpResponse
from django.template.loader import get_template

def parser(csvfile):
	# donor_objects = []
	donor_donation_count = 0
	donation_bulk = []
	donation_item_count = 0
	item_field_bulk = []
	item_bulk = []
	'''
	Helper Function
	Checks for existing donor matching the given parameter:
	- if exists, return donor_id
	- else, create new Donor object and return its donor_id
	'''
	def getCreateDonor(donor_name_f, email_f, want_receipt_f, telephone_number_f, mobile_number_f, address_line_f, city_f, province_f, postal_code_f, customer_ref_f):

		want_receipt_f = True if (want_receipt_f.lower() == "email") or (want_receipt_f.lower() == "e-mail") else False

		result_donor, unique = Donor.objects.get_or_create(donor_name = donor_name_f, email = email_f, want_receipt = want_receipt_f, telephone_number = telephone_number_f, mobile_number = mobile_number_f, address_line = address_line_f, city = city_f, province = province_f, postal_code=postal_code_f, customer_ref = customer_ref_f, verified=True)
		return result_donor

	'''
	Helper Function
	Checks for existing donation matching the given parameter:
	- if exists, return donation_id/tax_receipt_no
	- else, create new Donation object and return its donation_id/tax_receipt_no
	'''
	def addDonation(donor_f, tax_receipt_no_f, donate_date_f, pick_up_f):
		donate_date_f = parseDate(donate_date_f)
		result_donation = None
		try:
			result_donation = Donation.objects.get(tax_receipt_no=tax_receipt_no_f)
		except Donation.DoesNotExist:
			result_donation = Donation.objects.create(donor_id=donor_f, tax_receipt_no=tax_receipt_no_f, donate_date = donate_date_f, verified=True, pick_up = pick_up_f)
		# result_donation, unique = Donation.objects.get_or_create(donor_id=donor_f, tax_receipt_no=tax_receipt_no_f, donate_date = donate_date_f, verified=True, pick_up = pick_up_f)
		# donation_bulk.append(result_donation)
		return result_donation

	'''
	Helper Function
	Insert new Item using the parameters
	Returns nothing
	'''
	def addItem(donation_f, description_f, particulars_f, manufacturer_f, model_f, quantity_f, working_f, condition_f, quality_f, batch_f, value_f):
		working_f = True if (working_f == "Y") else False
		value_f = 0 if (not value_f) else value_f
		# item_field_bulk.append([donation_f, description_f, particulars_f, manufacturer_f, model_f, quantity_f, working_f, condition_f, quality_f, batch_f, value_f, True])
		item_bulk.append(Item(tax_receipt_no=donation_f, description = description_f, particulars = particulars_f, manufacturer=manufacturer_f, model=model_f, quantity=quantity_f, working=working_f,condition = condition_f, quality=quality_f, batch=batch_f, value=value_f, verified=True))

	def readyItem():
		result_donation = None
		count = 0
		for item in item_field_bulk:
			try:
				result_donation = Donation.objects.get(tax_receipt_no=donation_bulk[count])
			except Donation.DoesNotExist:
				result_donation = None
				print "Unexpected Problem"
			item_bulk.append(Item(tax_receipt_no=result_donation, description = description_f, particulars = particulars_f, manufacturer=manufacturer_f, model=model_f, quantity=quantity_f, working=working_f,condition = condition_f, quality=quality_f, batch=batch_f, value=value_f, verified=True))
			count += 1


	'''
	Helper Function
	Takes verbose date
	Returns string
	'''
	def parseDate(date_f):
		date_f = date_f.split(", ")[1]
		date_f = date_f.split(" ")

		months = {"January": "01","February": "02","March": "03","April": "04","May": "05","June": "06","July": "07","August": "08","September": "09","October": "10","November": "11","December": "12"}

		result = date_f[2] + "-" + months.get(date_f[1]) + "-" + date_f[0]
		return result

	# Use the 10b dummy.csv
	numline = len(list(csv.reader(csvfile, delimiter = ',')))
	read_file = csv.reader(csvfile, delimiter = ',')
	rowcount = 0
	verified = True
	# Donor Variables - verified is same for all
	donor_name_f, email_f, want_receipt_f, telephone_number_f, mobile_number_f, address_line_f, city_f, province_f, postal_code_f, customer_ref_f = None,None,None,None,None,None,None,None,None,None
	# Donation Variables - verified is same for all - donor_id pull from donor
	tax_receipt_no_f, donate_date_f, donor_city_f, pick_up_f = None,None,None, None
	# Item Variables - verified is same for all - tax_receipt_no pull from donation
	description_f, particulars_f, manufacturer_f, model_f, quantity_f, working_f, condition_f, quality_f, batch_f, value_f = None,None,None,None,None,None,None,None,None,None

	for row in read_file:
		# print numline
		if(0 < rowcount and rowcount <= numline):
			donor_name_f         = unicode(row[4],  "utf-8", errors='ignore')
			email_f              = unicode(row[15], "utf-8", errors='ignore')
			want_receipt_f       = unicode(row[14], "utf-8", errors='ignore')
			telephone_number_f   = unicode(row[11], "utf-8", errors='ignore')
			mobile_number_f      = unicode(row[12], "utf-8", errors='ignore')
			address_line_f       = unicode(row[5],  "utf-8", errors='ignore')
			city_f               = unicode(row[7],  "utf-8", errors='ignore')
			province_f           = unicode(row[8],  "utf-8", errors='ignore')
			pick_up_f			 = unicode(row[13], "utf-8", errors='ignore')
			postal_code_f        = unicode(row[9],  "utf-8", errors='ignore')
			tax_receipt_no_f     = unicode(row[1],  "utf-8", errors='ignore')
			donate_date_f        = unicode(row[3],  "utf-8", errors='ignore')
			description_f        = unicode(row[21], "utf-8", errors='ignore')
			particulars_f		 = unicode(row[22], "utf-8", errors='ignore')
			manufacturer_f       = unicode(row[17], "utf-8", errors='ignore')
			model_f              = unicode(row[20], "utf-8", errors='ignore')
			quantity_f           = unicode(row[16], "utf-8", errors='ignore')
			working_f            = unicode(row[23], "utf-8", errors='ignore')
			condition_f          = unicode(row[24], "utf-8", errors='ignore')
			quality_f            = unicode(row[25], "utf-8", errors='ignore')
			batch_f              = unicode(row[26], "utf-8", errors='ignore')
			value_f              = unicode(row[27], "utf-8", errors='ignore')
			customer_ref_f		 = unicode(row[28], "utf-8", errors='ignore')
			donor_f = getCreateDonor(donor_name_f, email_f, want_receipt_f, telephone_number_f, mobile_number_f, address_line_f, city_f, province_f, postal_code_f,customer_ref_f);
			donation_f = addDonation(donor_f, tax_receipt_no_f, donate_date_f, pick_up_f)
			addItem(donation_f, description_f, particulars_f, manufacturer_f, model_f, quantity_f, working_f, condition_f, quality_f, batch_f, value_f)
		rowcount += 1
		print "Parsed row #" + str(rowcount) + " (Added Donor & Donation)"
	print "Adding all items"
	list_of_items = Item.objects.bulk_create(item_bulk)
	print "Parsing Completed"
	return

def render_to_pdf(template_src,tax_no, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		response = HttpResponse(result.getvalue(), content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename=Tax Receipt '+ tax_no +'.pdf'
		return response
	return None

def generate_zip(pdf_array, pdf_array_names):
	# Open HttpResponse
	response = HttpResponse(content_type='application/zip')
	# Get date
	today = datetime.date.today()
	today_date = str(today.year) + "-" + str(today.month) + "-" + str(today.day)
	# Set correct content-disposition
	zip_csv_filename = 'Tax Receipts ' + today_date + '.zip'
	response['Content-Disposition'] = 'attachment; filename=' + zip_csv_filename
	# Open the file, writable
	zip = zipfile.ZipFile(response, 'w')

	idx = 0
	for name in pdf_array_names:
		zip.writestr(name, pdf_array[idx].getvalue())
		idx += 1

	# Must close zip for all contents to be written
	zip.close()

	return response
