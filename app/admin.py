# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Donor
from .models import Donation
from .models import Item

# Register your models here.


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
					'want_receipt')
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
		(None, 			{'fields': []})
	]
	list_display 	= ('business',
                    'first_name',
					'last_name',
					'email',
					'mobile_number',
					'receipt_id',
					'want_receipt')
	list_filter 	= ['business',
						'city',
						'receipt_id',
						'donate_date']
	search_fields 	= ['business',
					'donation_id',
					'receipt_id',
					'email']

class ItemAdmin(admin.ModelAdmin):
	def get_item(self, obj):
        	return obj.id

admin.site.register(Donor, DonorAdmin)
admin.site.register(Donation)
admin.site.register(Item, )
