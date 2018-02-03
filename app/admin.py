# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .models import Donor, Donation, Item

from django.contrib import admin
from django.http import HttpResponse
from django.views.generic import View
from django.http import HttpResponseRedirect, HttpResponse
from .utils import *
from views import start_pdf_gen
from django.core.urlresolvers import reverse
import datetime
import StringIO
import os
from django.shortcuts import redirect

# TO HIDE CELERY MENU FROM ADMIN PANEL
from django.contrib import admin
from djcelery.models import (
    TaskState, WorkerState, PeriodicTask,
    IntervalSchedule, CrontabSchedule)

admin.site.unregister(TaskState)
admin.site.unregister(WorkerState)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(PeriodicTask)



# Register your models here.
# Action for verification
def make_verified(modeladmin, request, queryset):
    queryset.update(verified=True)
    dlist = Donor.objects.all()
    for d in dlist:
        d.save()


make_verified.short_description = "Mark as verified"

# Action for unverification
def make_unverified(modeladmin, request, queryset):
    queryset.update(verified=False)
    dlist = Donor.objects.all()
    for d in dlist:
        d.save()


make_unverified.short_description = "Mark as unverified"

# Action for generating pdf
def generate_pdf(modeladmin, request, queryset):
    request.queryset = queryset
    return start_pdf_gen(request)

generate_pdf.short_description = "Generate Tax Receipt"





class DonorAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Donor Contacts',   {'fields': [
         'donor_name', 'email', 'telephone_number', 'mobile_number', 'customer_ref']}),
        ('Details', 	     {'fields': ['want_receipt']}),
        ('Address',          {'fields': [
            'address_line', 'city', 'province', 'postal_code']})
    ]
    list_display = ('id',
                    'donor_name',
                    'email',
                    'mobile_number',
                    'telephone_number',
                    'want_receipt',
                    'customer_ref',
                    'verified')
    list_filter = ['want_receipt', 'province']
    search_fields = ['id', 'donor_name', 'telephone_number', 'mobile_number',
                     'address_line', 'city', 'province', 'postal_code', 'customer_ref', 'email', ]

    def get_donor(self, obj):
        return obj.id
    get_donor.short_description = 'Donor ID'


class DonationAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Donation", 	{'fields': ['donor_id', 'get_donation_donor_name', 'tax_receipt_no', 'donate_date', 'verified', 'pick_up']})]
    actions = [make_verified, make_unverified, generate_pdf]

    list_display = ('donor_id',
                    'get_donation_donor_name',
                    'tax_receipt_no',
                    'donate_date',
                    'pick_up',
                    'verified')
    readonly_fields = ('get_donation_donor_name',)
    list_filter = ['pick_up', 'verified']
    search_fields = ['donor_id__donor_name', 'tax_receipt_no', 'donate_date', ]

    def get_donation_donor_name(self, obj):
        return obj.donor_id.donor_name
    get_donation_donor_name.short_description = 'Donor Name'


class ItemAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Item", 	{'fields': ['tax_receipt_no', 'description', 'particulars',
                              'manufacturer', 'model', 'quantity', 'working',
                              'condition', 'quality', 'verified', 'batch', 'value']}),
    ]

    list_display = ('get_item',
                    'tax_receipt_no',
                    'manufacturer',
                    'model',
                    'quantity',
                    'batch',
                    'verified',
                    'get_donor_name')
    list_filter = ['working', 'verified', 'quality']
    search_fields = ['manufacturer', 'model', 'working', 'batch',
                     'tax_receipt_no__tax_receipt_no', 'tax_receipt_no__donor_id__donor_name']

    def get_item(self, obj):
        return obj.id
    get_item.short_description = 'Item Id'

    actions = [make_verified, make_unverified]

    def get_donor_name(self, obj):
        return obj.tax_receipt_no.donor_id.donor_name
    get_donor_name.short_description = 'Donor Name'


admin.site.register(Donor, DonorAdmin)

# gave parameters for donation and item so verified could be accessed from admin panel
admin.site.register(Donation, DonationAdmin)

admin.site.register(Item, ItemAdmin)
