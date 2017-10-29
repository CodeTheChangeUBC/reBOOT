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
make_verified.short_description = "Mark as verified"

#Action for unverification
def make_unverified(modeladmin, request, queryset):
    queryset.update(verified = False)
make_unverified.short_description = "Mark as unverified"

class DonorAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, 			{'fields': ['business','first_name', 'last_name']}),
		('Details', 	{'fields': ['want_receipt']}),
		('Contacts', 	{'fields': ['email', 'telephone_number', 'mobile_number']}),
        ('Address',     {'fields': ['address_line1', 'address_line2', 'city', 'province', 'postal_code']})
	]
	list_display 	= ('get_donor',
					'business',
                    'first_name',
					'last_name',
					'email',
					'mobile_number',
					'want_receipt',
                    'verified')
	list_filter 	= ['business',
						'city']
	search_fields 	= ['business',
					'get_donor',
					'receipt_id',
					'email']
	def get_donor(self, obj):
        	return obj.id

class DonationAdmin(admin.ModelAdmin):
    fieldsets = [
		(None, 	{'fields': ['donor_id', 'tax_receipt_no', 'donate_date', 'donor_city', 'verified']})
    ]
    actions = [make_verified, make_unverified]


    list_display 	= ('donor_id',
                       'tax_receipt_no',
                       'donate_date',
                       'donor_city',
                       'verified')

    list_filter = ['donor_id', 'donate_date', 'tax_receipt_no',]
    search_fields 	= ['business',
					'donation_id',
					'receipt_id',
					'email']



class ItemAdmin(admin.ModelAdmin):
    def get_item(self, obj):
        return obj.id
    list_display = ['quantity', 'tax_receipt_no', 'quality', 'verified']
    actions = [make_verified, make_unverified]

admin.site.register(Donor, DonorAdmin)

#gave parameters for donation and item so verified could be accessed from admin panel
admin.site.register(Donation, DonationAdmin )

admin.site.register(Item, ItemAdmin)
