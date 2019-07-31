# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib import admin
from rangefilter.filter import DateRangeFilter

from app.constants.str import (
    PERMISSION_DENIED, UNVERIFIED_DONATION, RECEIPTED_DONATION)
from app.models import (
    Donor, Donation, Item, ItemDevice, ItemDeviceType)
from app.utils import *
from app.views.views import generate_receipt


class DonorAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Contact', {'fields': (
            'donor_name',
            'contact_name',
            'email',
            'mobile_number',
            'telephone_number',
            'customer_ref',)}),
        ('Address', {'fields': (
            'address_line_one',
            'address_line_two',
            'city',
            'province',
            'postal_code',)}),
        ('Others', {'fields': ('want_receipt',)}),
    )
    list_per_page = 25
    list_display = ('id',
                    'donor_name',
                    'contact_name',
                    'email',
                    'mobile_number',
                    'telephone_number',
                    'want_receipt',
                    'get_verified',
                    'customer_ref',
                    'donation_count',
                    'item_count')
    list_filter = (('updated_at', DateRangeFilter), 'want_receipt', 'province')
    search_fields = (
        'donor_name',
        'contact_name',
        'email',
        'telephone_number',
        'mobile_number',
        'address_line_one',
        'address_line_two',
        'city',
        'postal_code',
        'customer_ref',)

    def get_verified(self, obj):
        return obj.verified
    get_verified.boolean = True
    get_verified.short_description = 'Verified?'

    def donation_count(self, obj):
        return obj.donation_set.count()
    donation_count.short_description = '# of Donation(s)'

    def item_count(self, obj):
        count_per_donor = sum([
            donation.item_set.count() for donation in obj.donation_set.all()
        ])
        return count_per_donor
    item_count.short_description = '# of Item(s)'


class DonationAdmin(admin.ModelAdmin):
    raw_id_fields = ('donor',)
    fieldsets = (
        ('Donor',
            {'fields': ('donor',)}),
        ('Donation',
            {'fields': ('tax_receipt_no', 'source', 'pledge_date',
                        'donate_date', 'pick_up')}))
    actions = ('make_items_unverified', 'make_items_verified', 'generate_pdf')

    list_per_page = 25
    list_display = ('tax_receipt_no',
                    'donor_id',
                    'donor',
                    'source',
                    'pledge_date',
                    'donate_date',
                    'pick_up',
                    'get_verified',
                    'item_count',
                    'tax_receipt_created_at',)
    list_filter = (('donate_date', DateRangeFilter),
                   ('pledge_date', DateRangeFilter),
                   ('tax_receipt_created_at', DateRangeFilter),
                   'source',
                   'pick_up',)
    search_fields = ('donor__donor_name', 'tax_receipt_no',)

    def get_verified(self, obj):
        return obj.verified
    get_verified.boolean = True
    get_verified.short_description = 'Verified?'

    def donor_id(self, obj):
        return obj.donor.id
    donor_id.short_description = 'Donor ID'

    def item_count(self, obj):
        return obj.item_set.count()
    item_count.short_description = '# of Item(s)'

    def make_items_unverified(self, req, qs):
        update_cnt = sum([
            obj.item_set.update(verified=False) for obj in qs
        ])
        msg = "1 item was" if update_cnt == 1 else "%s items were" % update_cnt
        self.message_user(req, "%s successfully marked as unverified." % msg)
    make_items_unverified.short_description = 'Mark related items as unverified'

    def make_items_verified(self, req, qs):
        update_cnt = sum([
            obj.item_set.update(verified=True) for obj in qs
        ])
        msg = "1 item was" if update_cnt == 1 else "%s items were" % update_cnt
        self.message_user(req, "%s successfully marked as verified." % msg)
    make_items_verified.short_description = 'Mark related items as verified'

    def generate_pdf(self, req, qs):
        if not req.user.has_perm('app.generate_tax_receipt'):
            return self.message_user(
                req, PERMISSION_DENIED, level=messages.ERROR)

        req.queryset = qs
        # TODO: Replace this check. Add check for verified prop, item verified,
        # item valuation date
        not_verified_donations = qs.filter(verified=False)
        if not_verified_donations:
            return self.message_user(
                req, UNVERIFIED_DONATION, level=messages.ERROR)

        tr_already_generated = qs.exclude(tax_receipt_created_at__isnull=True)
        if tr_already_generated:
            return self.message_user(
                req, RECEIPTED_DONATION, level=messages.ERROR)

        return generate_receipt(req)
    generate_pdf.short_description = "Generate Tax Receipt(s)"


class ItemAdmin(admin.ModelAdmin):
    raw_id_fields = ('donation', 'device')
    fieldsets = (
        ('Donation', {'fields': ('donation',)}),
        ('Device', {'fields': ('device',)}),
        ('Item Details', {'fields': ('quantity',
                                     ('verified', 'working',),
                                     'serial_number',
                                     'asset_tag',
                                     'particulars',
                                     'quality',
                                     'condition',
                                     'batch',
                                     'status',)}),
        ('Valuation', {'fields': ('value', 'valuation_date',
                                  'valuation_supporting_doc',)}))
    # TODO: Add a add_view() to control based on user permission to set value
    if False:
        readonly_fields = ['value',
                           'valuation_date',
                           'valuation_supporting_doc']

    list_per_page = 25
    list_display = ('id',
                    'donation',
                    'donor_name',
                    'device',
                    'quantity',
                    'status',
                    'verified',
                    'serial_number',
                    'batch')
    list_filter = (('donation__donate_date', DateRangeFilter),
                   'verified',
                   'working',
                   'quality')
    search_fields = ('device__model',
                     'device__make',
                     'batch',
                     'donation__tax_receipt_no',
                     'donation__donor__donor_name')

    actions = ('make_verified', 'make_unverified', 'make_pledged',
               'make_received', 'make_tested', 'make_refurbished', 'make_sold',
               'make_recycled')

    def get_item(self, obj):
        return obj.id
    get_item.short_description = 'Item ID'

    def donor_name(self, obj):
        return obj.donation.donor.donor_name
    donor_name.short_description = 'Donor Name'

    def make_verified(self, req, qs):
        qs.update(verified=True)
        dlist = Donor.objects.all()
        for d in dlist:
            d.save()
    make_verified.short_description = "Mark as verified"

    def make_unverified(self, req, qs):
        qs.update(verified=False)
        dlist = Donor.objects.all()
        for d in dlist:
            d.save()
    make_unverified.short_description = "Mark as unverified"

    def make_pledged(self, req, qs):
        if not req.user.has_perm('app.update_status'):
            return self.message_user(
                req,
                PERMISSION_DENIED,
                level=messages.ERROR
            )
        update_cnt = qs.update(status='pledged')
        msg = "1 row was" if update_cnt == 1 else "%s rows were" % update_cnt
        self.message_user(req, "%s successfully marked as pledged." % msg)
    make_pledged.short_description = "Mark as pledged"

    def make_received(self, req, qs):
        update_cnt = qs.update(status='received')
        msg = "1 row was" if update_cnt == 1 else "%s rows were" % update_cnt
        self.message_user(req, "%s successfully marked as received." % msg)
    make_received.short_description = "Mark as received"

    def make_tested(self, req, qs):
        update_cnt = qs.update(status='tested')
        msg = "1 row was" if update_cnt == 1 else "%s rows were" % update_cnt
        self.message_user(req, "%s successfully marked as tested." % msg)
    make_tested.short_description = "Mark as tested"

    def make_refurbished(self, req, qs):
        update_cnt = qs.update(status='refurbished')
        msg = "1 row was" if update_cnt == 1 else "%s rows were" % update_cnt
        self.message_user(req, "%s successfully marked as refurbished." % msg)
    make_refurbished.short_description = "Mark as refurbished"

    def make_sold(self, req, qs):
        update_cnt = qs.update(status='sold')
        msg = "1 row was" if update_cnt == 1 else "%s rows were" % update_cnt
        self.message_user(req, "%s successfully marked as sold." % msg)
    make_sold.short_description = "Mark as sold"

    def make_recycled(self, req, qs):
        update_cnt = qs.update(status='recycled')
        msg = "1 row was" if update_cnt == 1 else "%s rows were" % update_cnt
        self.message_user(req, "%s successfully marked as recycled." % msg)
    make_recycled.short_description = "Mark as recycled"


class ItemDeviceTypeAdmin(admin.ModelAdmin):
    fields = ('category', 'device_type')
    list_display = ('id', 'category', 'device_type')
    list_filter = ('category',)
    search_fields = ('category', 'device_type')


class ItemDeviceAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Device Type', {
            'fields': ('dtype',)}),
        ('Device Details', {
            'fields': ('make', 'model',)}),
        ('Conditional Details', {
            'fields': ('cpu_type', 'speed', 'memory', 'hd_size', 'screen_size',
                       'hdd_serial_number', 'operating_system',)}))

    list_display = ('id', 'dtype', 'make', 'model')
    list_filter = ('dtype', 'make')
    search_fields = ('dtype', 'make', 'model')


admin.site.register(Donor, DonorAdmin)
admin.site.register(Donation, DonationAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemDeviceType, ItemDeviceTypeAdmin)
admin.site.register(ItemDevice, ItemDeviceAdmin)
