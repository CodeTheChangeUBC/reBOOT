# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .models import Donor,Donation,Item

from django.contrib import admin
from django.http import HttpResponse
from django.views.generic import View

from .utils import render_to_pdf

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
	pdf_array = []
	pdf_array_names = []
	for row in queryset:
		data = {
			'today': row.donate_date,
			'amount': 39.99,
			'customer_name': 'Cooper Mann',
			'order_id': row.tax_receipt_no,
		}
		pdf = render_to_pdf('pdf/receipt.html', data)
		response = HttpResponse(pdf, content_type='application/pdf')
		pdf_array.append(response)
		# TODO: GET FILESNAMES
		pdf_array_names.append()
	if (len(pdf_array) == 1):
		return pdf_array[0]
	else:
		# Folder name in ZIP archive which contains the above files
		# E.g [thearchive.zip]/subdir/file2.txt
		zip_subdir = "Tax Receipts "# + datetime.date().today
		zip_filename = "%s.zip" % zip_subdir

		# Open StringIO to grab in-memory ZIP contents
		s = StringIO.StringIO()

		# The zip compressor
		zf = zipfile.ZipFile(s, "w")

		# FIXME: This isn't working yet.
		for fpath in pdf_array_names:
			# Calculate path for file in zip
			fdir, fname = os.path.split(fpath)
			zip_path = os.path.join(zip_subdir, fname)

			# Add file, at correct path
			zf.write(fpath, zip_path)

		# Must close zip for all contents to be written
		zf.close()

		# Grab ZIP file from in-memory, make response with correct MIME-type
		resp = HttpResponse(s.getvalue(), mimetype = "application/x-zip-compressed")
		# ..and correct content-disposition
		resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

		return resp
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
					'want_receipt',
					'verified')
	list_filter 	= ['city', 'province']
	search_fields 	= ['id','donor_name','email', 'telephone_number', 'mobile_number','address_line','city', 'province', 'postal_code']

	def get_donor(self, obj):
		return obj.id
	get_donor.short_description = 'Donor ID'

class DonationAdmin(admin.ModelAdmin):
    fieldsets = [
		("Donation", 	{'fields': ['donor_id', 'get_donation_donor_name', 'tax_receipt_no', 'donate_date', 'verified']})
    ]
    actions = [make_verified, make_unverified, generate_pdf]


    list_display 	= ('donor_id', 'get_donation_donor_name',
                       'tax_receipt_no',
                       'donate_date',
                       'verified')
    readonly_fields = ('get_donation_donor_name',)
    list_filter = []
    search_fields 	= ['donor_id', 'get_donation_donor_name','tax_receipt_no','donate_date',]


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
	list_filter 	= ['manufacturer']
	search_fields 	= ['tax_receipt_no','manufacturer','model', 'batch']



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
