# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .models import Donor,Donation,Item

from django.contrib import admin
from django.http import HttpResponse
from django.views.generic import View

from .utils import *

import datetime
import StringIO
import zipfile
import os


# Register your models here.
#Action for verification
def make_verified(modeladmin, request, queryset):
	queryset.update(verified = True)
	dlist = Donor.objects.all()
	for d in dlist:
		d.save()
make_verified.short_description = "Mark as verified"

#Action for unverification
def make_unverified(modeladmin, request, queryset):
	queryset.update(verified = False)
	dlist = Donor.objects.all()
	for d in dlist:
		d.save()
make_unverified.short_description = "Mark as unverified"

def generate_pdf(modeladmin, request, queryset):
	# Forward Variable declaration
	pdf_array = []
	pdf_array_names = []

	for row in queryset:
		listofitems = Item.objects.filter(tax_receipt_no = row.tax_receipt_no)
		totalvalue = 0
		for item in listofitems:
			totalvalue += item.value * item.quantity
		today = datetime.date.today()
		today_date = str(today.year) + "-" + str(today.month) + "-" + str(today.day)
		data = {
			'generated_date': today_date,
			'date': row.donate_date,
			'address': row.donor_id.address_line,
			'city': row.donor_id.city,
			'province': row.donor_id.province,
			'postalcode': row.donor_id.postal_code,
			'telephone': row.donor_id.telephone_number,
			'email': row.donor_id.email,
			'customer_name': row.donor_id.donor_name,
			'tax_receipt_no': row.tax_receipt_no,
			'listofitems': listofitems,
			'total': totalvalue,
			'customer_ref': row.donor_id.customer_ref,
		}
		response = render_to_pdf('pdf/receipt.html', row.tax_receipt_no, data)
		pdf_array.append(response)
		pdf_array_names.append("Tax Receipt " + row.tax_receipt_no + ".pdf")
	if (len(pdf_array) == 1):
		return pdf_array[0]
	else:
		# generate_zip defined in utils.py
		return generate_zip(pdf_array, pdf_array_names)
generate_pdf.short_description = "Generate Tax Receipt"



class DonorAdmin(admin.ModelAdmin):
	fieldsets = [
		('Donor Contacts',   {'fields': ['donor_name','email', 'telephone_number', 'mobile_number']}),
		('Details', 	     {'fields': ['want_receipt']}),
		('Address',          {'fields': ['address_line','city', 'province', 'postal_code']})
	]
	list_display 	= ('id',
						'donor_name',
						'email',
						'mobile_number',
						'telephone_number',
						'want_receipt',
						'verified')
	list_filter 	= ['want_receipt', 'province']
	search_fields   = ['id', 'donor_name', 'telephone_number', 'mobile_number', 'address_line', 'city', 'province', 'postal_code', 'email',]
	def get_donor(self, obj):
		return obj.id
	get_donor.short_description = 'Donor ID'

class DonationAdmin(admin.ModelAdmin):
	fieldsets = [
		("Donation", 	{'fields': ['donor_id', 'get_donation_donor_name', 'tax_receipt_no', 'donate_date', 'verified']})]
	actions = [make_verified, make_unverified, generate_pdf]


 	list_display 	= ('donor_id','get_donation_donor_name',
						'tax_receipt_no',
						'donate_date',
						'verified')
	readonly_fields = ('get_donation_donor_name',)
	list_filter = ['verified']
	search_fields 	= ['donor_id__donor_name','tax_receipt_no','donate_date',]


	def get_donation_donor_name(self, obj):
		return obj.donor_id.donor_name
	get_donation_donor_name.short_description = 'Donor Name'

class ItemAdmin(admin.ModelAdmin):
	fieldsets = [
		("Item", 	{'fields': ['tax_receipt_no', 'description', 'particulars',
							'manufacturer','model','quantity', 'working',
							'condition','quality','verified','batch','value']}),
	]

	list_display 	= ('get_item', 'tax_receipt_no', 'manufacturer', 'model', 'quantity', 'batch','verified', 'get_donor_name')
	list_filter 	= ['working','verified', 'quality']
	search_fields 	= ['manufacturer','model', 'working', 'batch', 'tax_receipt_no__tax_receipt_no', 'tax_receipt_no__donor_id__donor_name']




	def get_item(self, obj):
		return obj.id
	get_item.short_description = 'Item Id'


	actions = [make_verified, make_unverified]

	def get_donor_name(self, obj):
		return obj.tax_receipt_no.donor_id.donor_name
	get_donor_name.short_description = 'Donor Name'

admin.site.register(Donor, DonorAdmin)

#gave parameters for donation and item so verified could be accessed from admin panel
admin.site.register(Donation, DonationAdmin )

admin.site.register(Item, ItemAdmin)
