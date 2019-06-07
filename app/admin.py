# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from app.models import Donor, Donation, Item
from app.utils import *
from app.views.views import start_pdf_gen
from datetime import datetime


# TO HIDE CELERY MENU FROM ADMIN PANEL
from django.contrib import messages
from django.contrib import admin
from djcelery.models import (
    TaskState, WorkerState, PeriodicTask,
    IntervalSchedule, CrontabSchedule)

admin.site.unregister(TaskState)
admin.site.unregister(WorkerState)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(PeriodicTask)


def make_verified(modeladmin, request, queryset):
    queryset.update(verified=True)
    dlist = Donor.objects.all()
    for d in dlist:
        d.save()


make_verified.short_description = "Mark as verified"


def make_unverified(modeladmin, request, queryset):
    queryset.update(verified=False)
    dlist = Donor.objects.all()
    for d in dlist:
        d.save()


make_unverified.short_description = "Mark as unverified"


def make_pledge(modeladmin, request, queryset):
    queryset.update(status='pledged')


make_pledge.short_description = "Mark as pledged"


def make_received(modeladmin, request, queryset):
    queryset.update(status='received')


make_received.short_description = "Mark as received"


def make_tested(modeladmin, request, queryset):
    queryset.update(status='tested')


make_tested.short_description = "Mark as tested"


def make_refurbished(modeladmin, request, queryset):
    queryset.update(status='refurbished')


make_refurbished.short_description = "Mark as refurbished"


def make_sold(modeladmin, request, queryset):
    queryset.update(status='sold')


make_sold.short_description = "Mark as sold"


def make_recycled(modeladmin, request, queryset):
    queryset.update(status='recycled')


make_recycled.short_description = "Mark as recycled"


def generate_pdf(modeladmin, request, queryset):
    if not request.user.has_perm('app.generate_tax_receipt'):
        return messages.error(request, 'Permission denied. Please contact admin for access.')

    request.queryset = queryset
    request.modeladmin = modeladmin

    not_verified_donations = queryset.filter(verified=False)
    if not_verified_donations:
        return messages.error(request, 'Unverified donations are not valid for tax receipt generation. Please review and try again.')

    tax_receipts_already_generated = queryset.exclude(
        tax_receipt_created_at__isnull=True)
    if tax_receipts_already_generated:
        return messages.error(request, 'Donations with tax receipts already generated are not valid for tax receipt generation. Please review and try again.')

    queryset.update(tax_receipt_created_at=datetime.now())
    return start_pdf_gen(request)


generate_pdf.short_description = "Generate Tax Receipt"


class DonorAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Donor Contacts', {'fields': [
         'donor_name', 'email', 'telephone_number', 'mobile_number', 'customer_ref']}),
        ('Details', {'fields': ['want_receipt']}),
        ('Address', {'fields': [
            'address_line', 'city', 'province', 'postal_code']})
    ]
    list_display = ('id',
                    'donor_name',
                    'email',
                    'mobile_number',
                    'telephone_number',
                    'want_receipt',
                    'customer_ref',
                    'verified',
                    'item_count')
    list_filter = ['want_receipt', 'province']
    search_fields = ['id', 'donor_name', 'telephone_number', 'mobile_number',
                     'address_line', 'city', 'province', 'postal_code', 'customer_ref', 'email']

    def item_count(self, obj):
        count_per_donor = sum([
            donation.item_set.count() for donation in obj.donation_set.all()
        ])
        return count_per_donor
    item_count.short_description = '# of Item(s)'


class DonationAdmin(admin.ModelAdmin):
    raw_id_fields = ('donor',)
    fieldsets = [
        ('Donor',
            {'fields': ['donor', 'donor_name']}),
        ('Donation',
            {'fields': ['tax_receipt_no', 'donate_date', 'verified', 'pick_up']})]
    actions = [make_verified, make_unverified, generate_pdf]

    list_display = ('tax_receipt_no',
                    'donor',
                    'donor_name',
                    'donate_date',
                    'pick_up',
                    'verified',
                    'item_count')
    readonly_fields = ('donor_name',)
    list_filter = ['pick_up', 'verified']
    search_fields = ['donor__donor_name', 'tax_receipt_no', 'donate_date', ]

    def donor_name(self, obj):
        return obj.donor.donor_name
    donor_name.short_description = 'Donor Name'

    def item_count(self, obj):
        return obj.item_set.count()
    item_count.short_description = '# of Item(s)'


class ItemAdmin(admin.ModelAdmin):
    raw_id_fields = ('donation',)
    fieldsets = [
        ("Item", {'fields': ['donation', 'description', 'particulars',
                             'manufacturer', 'model', 'quantity', 'working',
                             'condition', 'quality', 'verified', 'batch', 'value']})]

    list_display = ('get_item',
                    'donation',
                    'manufacturer',
                    'model',
                    'quantity',
                    'status',
                    'verified',
                    'donor_name',
                    'batch'
                    )
    list_filter = ['working', 'verified', 'quality']
    search_fields = ['manufacturer', 'model', 'working', 'batch',
                     'donation__tax_receipt_no', 'donation__donor__donor_name']

    actions = [
        make_verified,
        make_unverified,
        make_pledge,
        make_received,
        make_tested,
        make_refurbished,
        make_sold,
        make_recycled
    ]

    def get_item(self, obj):
        return obj.id
    get_item.short_description = 'Item Id'

    def donor_name(self, obj):
        return obj.donation.donor.donor_name
    donor_name.short_description = 'Donor Name'


admin.site.register(Donor, DonorAdmin)
admin.site.register(Donation, DonationAdmin)
admin.site.register(Item, ItemAdmin)
