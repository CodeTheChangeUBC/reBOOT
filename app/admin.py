# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Donor
from .models import Donation
from .models import Item


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







class DonorAdmin(admin.ModelAdmin):
	fieldsets = [
		('Donor Contacts',   {'fields': ['donor_name','email', 'telephone_number', 'mobile_number']}),
		('Details', 	     {'fields': ['want_receipt']}),
        ('Address',          {'fields': ['address_line','city', 'province', 'postal_code']})
	]
	list_display 	= ('get_donor',
                    'donor_name',
					'email',
					'mobile_number',
					'want_receipt',
					   'verified')
	list_filter 	= ['city']
	search_fields 	= ['get_donor',
					'receipt_id',
					'email']

	def get_donor(self, obj):
		return obj.id
	get_donor.short_description = 'Donor ID'

class DonationAdmin(admin.ModelAdmin):
    fieldsets = [
		(None, 	{'fields': ['donor_id', 'get_donation_donor_name', 'tax_receipt_no', 'donate_date', 'donor_city', 'verified']})
    ]
    actions = [make_verified, make_unverified]


    list_display 	= ('donor_id', 'get_donation_donor_name',
                       'tax_receipt_no',
                       'donate_date',
                       'donor_city',
                       'verified')
    readonly_fields = ('get_donation_donor_name',)
    list_filter = ['donor_id', 'donate_date', 'tax_receipt_no',]
    search_fields 	= ['donation_id', 'receipt_id', 'email']


    def get_donation_donor_name(self, obj):
        return obj.donor_id.donor_name
    get_donation_donor_name.short_description = 'Donor Name'

class ItemAdmin(admin.ModelAdmin):

	fieldsets = [
		(None, 			{'fields': ['tax_receipt_no', 'description', 'manufacturer', 'model',
                                    'quantity', 'working', 'condition','quality','verified',
                                    'batch','value']}),
		#('donation information', 	{'fields': ['get_item', 'get_donor_lname', 'get_donor_fname']}),
		# ('Strangepropertylol', 		{'fields': []}),
	]


	list_display 	= ('get_item', 'tax_receipt_no', 'quantity', 'quality','verified', 'get_donor_name')
	list_filter 	= ['manufacturer', 'model', 'working','verified']
	search_fields 	= ['manufacturer','model', 'working']



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
