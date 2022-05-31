# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib import admin
from django.db import models
from django.http import HttpResponseRedirect, HttpRequest
from django.forms import Textarea
from django.utils import timezone as tz
from rangefilter.filter import DateRangeFilter

from app.constants.str import (
    PERMISSION_DENIED, UNVERIFIED_DONATION, RECEIPTED_DONATION,
    UNEVALUATED_DONATION, EMPTY_DONATION, ITEM_NOT_RECEIVED)
from app.enums import ItemStatusEnum
from app.models import (
    Donor, Donation, Item, ItemDevice, ItemDeviceType)
from app.filters import DonorBusinessFilter, DonationStatusFilter
from app.views.views import download_receipt, export_csv
from app.widgets.CustomForeignKeyRawIdWidget import CustomForeignKeyRawIdWidget


class ResourceAdmin(admin.ModelAdmin):
    save_on_top = True
    list_per_page = 100
    list_max_show_all = 200

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        db = kwargs.get('using')
        kwargs['widget'] = CustomForeignKeyRawIdWidget(
            db_field.remote_field, self.admin_site, using=db,
        )
        return super(ResourceAdmin, self).formfield_for_foreignkey(
            db_field, request=request, **kwargs)


class DonationInline(admin.TabularInline):
    model = Donation
    extra = 0
    show_change_link = True

    readonly_fields = ('tax_receipt_created_at', 'status',)
    fields = ('tax_receipt_no', 'status', 'pledge_date', 'donate_date',
              'pick_up', 'tax_receipt_created_at', 'source')


class DonorAdmin(ResourceAdmin):
    inlines = (DonationInline,)

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
    list_display = ('id',
                    'donor_name',
                    'contact_name',
                    'email',
                    'mobile_number',
                    'telephone_number',
                    'want_receipt',
                    'verified',
                    'customer_ref',
                    'donation_count',
                    'item_count')
    list_filter = (('updated_at', DateRangeFilter),
                   DonorBusinessFilter,
                   'want_receipt',
                   'province')
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
    actions = ('destroy_donor',)

    def donation_count(self, obj):
        return obj.donation_set.count()
    donation_count.short_description = '# of Donation(s)'

    def item_count(self, obj):
        count_per_donor = sum([
            donation.item_set.count() for donation in obj.donation_set.all()
        ])
        return count_per_donor
    item_count.short_description = '# of Item(s)'

    def destroy_donor(self, req: HttpRequest, qs):
        if not req.user.has_perm('app.destroy_donor'):
            return self.message_user(
                req, PERMISSION_DENIED, level=messages.ERROR)

        count, detail = qs.destroy()
        return self.message_user(
            req,
            f"{count} object(s) destroyed. Related detail: {detail}",
            level=messages.SUCCESS
        )
    destroy_donor.short_description = "Destroy Donor(s)"


class ItemInline(admin.TabularInline):
    model = Item
    extra = 0
    show_change_link = True
    raw_id_fields = ('device',)

    fields = ('status', 'quantity', 'device', 'serial_number', 'quality',
              'working', 'condition', 'notes', 'value',
              'valuation_supporting_doc', 'valuation_date')

    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(attrs={'rows': 1, 'style': 'height: 1em;'})}}

    def get_readonly_fields(self, req, obj=None):
        return _get_readonly_item_fields(self, req, obj)


class DonationAdmin(ResourceAdmin):
    change_form_template = "admin/extras/donations_change_form.html"
    inlines = (ItemInline,)
    raw_id_fields = ('donor',)
    readonly_fields = ('donor_contact_name', 'donor_donor_name', 'donor_email',
                       'donor_mobile_number', 'status',)

    fieldsets = (
        ('Donor',
            {'fields': ('donor', 'donor_contact_name', 'donor_donor_name',
                        'donor_email', 'donor_mobile_number',)}),
        ('Donation',
            {'fields': ('tax_receipt_no', 'source', 'pick_up', 'status',
                        'pledge_date', 'donate_date', 'test_date',
                        'valuation_date', 'tax_receipt_created_at', 'notes')}))
    actions = ('mark_items_unverified', 'mark_items_verified', 'generate_csv',
               'generate_receipt', 'destroy_donation')

    list_display = ('tax_receipt_no',
                    'donor_id',
                    'donor',
                    'status',
                    'pledge_date',
                    'tax_receipt_created_at',
                    'pick_up',
                    'total_value', # total value of donation
                    'verified',
                    'item_count',
                    'donate_date',
                    'test_date',
                    'valuation_date',
                    'source',)
    list_filter = (DonationStatusFilter,
                   ('pledge_date', DateRangeFilter),
                   ('donate_date', DateRangeFilter),
                   ('test_date', DateRangeFilter),
                   ('valuation_date', DateRangeFilter),
                   ('tax_receipt_created_at', DateRangeFilter),
                   'source',)
    search_fields = (
        'donor__contact_name',
        'donor__donor_name',
        'tax_receipt_no',
        'pick_up')

    def donor_id(self, obj):
        return obj.donor.id
    donor_id.short_description = 'Donor ID'

    def donor_contact_name(self, obj):
        return obj.donor.contact_name
    donor_contact_name.short_description = 'Contact Name'

    def donor_donor_name(self, obj):
        return obj.donor.donor_name
    donor_donor_name.short_description = 'Donor Name'

    def donor_email(self, obj):
        return obj.donor.email
    donor_email.short_description = 'Email'

    def donor_mobile_number(self, obj):
        return obj.donor.mobile_number
    donor_mobile_number.short_description = 'Mobile Number'

    def item_count(self, obj):
        return obj.item_set.count()
    item_count.short_description = '# of Item(s)'

    def _mark_items_verified_base(self, req, qs, verified):
        update_cnt = sum([
            obj.item_set.update(verified=verified) for obj in qs
        ])
        msg = "1 item was" if update_cnt == 1 else "%s items were" % update_cnt
        marked_as = "verified" if verified else "unverified"
        self.message_user(
            req, "%s successfully marked as %s." % (msg, marked_as))

    def mark_items_verified(self, req, qs):
        self._mark_items_verified_base(req, qs, True)
    mark_items_verified.short_description = 'Mark related items as verified'

    def mark_items_unverified(self, req, qs):
        self._mark_items_verified_base(req, qs, False)
    mark_items_unverified.short_description = \
        'Mark related items as unverified'

    def generate_receipt_policy(self, req, qs):
        err = None
        if not req.user.has_perm('app.generate_tax_receipt'):
            err = PERMISSION_DENIED
        elif not all([d.is_items_received() for d in qs]):
            err = ITEM_NOT_RECEIVED
        elif not all([d.verified() for d in qs]):
            err = UNVERIFIED_DONATION
        elif not all([d.evaluated() for d in qs]):
            err = UNEVALUATED_DONATION
        elif not all([d.valuation_date for d in qs]):
            err = UNEVALUATED_DONATION
        elif bool(qs.exclude(tax_receipt_created_at__isnull=True)):
            err = RECEIPTED_DONATION
        elif not all([d.item_set.exists() for d in qs]):
            err = EMPTY_DONATION
        return err

    def generate_receipt(self, req, qs):
        err = self.generate_receipt_policy(req, qs)
        if err:
            return self.message_user(req, err, level=messages.ERROR)
        req.queryset = qs
        return download_receipt(req)
    generate_receipt.short_description = "Generate Tax Receipt(s)"

    def generate_csv_policy(self, req: HttpRequest):
        err = None
        if not req.user.has_perm('app.can_export_data'):
            err = PERMISSION_DENIED
        return err

    def generate_csv(self, req: HttpRequest, qs):
        err = self.generate_csv_policy(req)
        if err:
            return self.message_user(req, err, level=messages.ERROR)
        req.POST._mutable = True
        req.POST["export_name"] = f"{tz.localdate().isoformat()} reBOOT data"
        req.queryset = Item.objects.filter(donation__in=qs)
        req.POST._mutable = False
        return export_csv(req)
    generate_csv.short_description = "Export selected data as CSV"

    def destroy_donation(self, req: HttpRequest, qs):
        if not req.user.has_perm('app.destroy_donor'):
            return self.message_user(
                req, PERMISSION_DENIED, level=messages.ERROR)

        count, detail = qs.destroy()
        return self.message_user(
            req,
            f"{count} object(s) destroyed. Related detail: {detail}",
            level=messages.SUCCESS
        )
    destroy_donation.short_description = "Destroy Donation(s)"

    def response_change(self, req: HttpRequest, obj):
        if "_generate_receipt" in req.POST or \
           "_mark_items_verified" in req.POST or \
           "_mark_items_unverified" in req.POST:
            obj.save()
            qs = self.get_queryset(req).filter(pk=obj.pk)
            if "_generate_receipt" in req.POST:
                err = self.generate_receipt_policy(req, qs)
                if err:
                    self.message_user(req, err, level=messages.ERROR)
                    return HttpResponseRedirect(".")
                req.queryset = qs
                return download_receipt(req)
            elif "_mark_items_verified" in req.POST:
                self.mark_items_verified(req, qs)
                return HttpResponseRedirect(".")
            elif "_mark_items_unverified" in req.POST:
                self.mark_items_unverified(req, qs)
                return HttpResponseRedirect(".")
        else:
            return super().response_change(req, obj)

    def get_readonly_fields(self, req: HttpRequest, obj=None):
        return _get_readonly_donation_fields(self, req, obj)


class ItemAdmin(ResourceAdmin):
    raw_id_fields = ('donation', 'device')
    readonly_fields = ('donor_name', 'contact_name', 'email', 'mobile_number')

    fieldsets = (
        ('Donation', {'fields': ('donation', 'donor_name',
                                 'contact_name', 'email', 'mobile_number')}),
        ('Item Details', {'fields': ('status',
                                     'quantity',
                                     'device',
                                     'serial_number',
                                     'working',
                                     'quality',
                                     'condition',
                                     'notes',)}),
        ('Valuation', {'fields': ('value', 'valuation_date',
                                  'valuation_supporting_doc',)}),
        ('Legacy/Extra Fields', {'fields': ('weight',
                                            'asset_tag',
                                            'batch',
                                            'particulars',)}))

    list_display = ('id',
                    'donation',
                    'donor_name',
                    'device',
                    'quantity',
                    'value',
                    'status',
                    'valuation_date',
                    'serial_number',
                    'verified',)
    list_filter = (('donation__donate_date', DateRangeFilter),
                   ('donation__valuation_date', DateRangeFilter),
                   'status',
                   'working',
                   'verified',
                   'quality',)
    search_fields = ('device__model',
                     'device__make',
                     'donation__tax_receipt_no',
                     'donation__donor__donor_name')

    actions = ('mark_verified', 'mark_unverified', 'mark_pledged',
               'mark_received', 'mark_tested', 'mark_refurbished', 'mark_sold',
               'mark_recycled', 'destroy_item')

    def get_readonly_fields(self, req, obj=None):
        return _get_readonly_donation_fields(self, req, obj)

    def get_item(self, obj):
        return obj.id
    get_item.short_description = 'Item ID'

    def valuation_date(self, obj):
        return obj.donation.valuation_date
    valuation_date.short_description = 'Valuation Date'

    def donor_name(self, obj):
        return obj.donation.donor.donor_name
    donor_name.short_description = 'Donor Name'

    def contact_name(self, obj):
        return obj.donation.donor.contact_name
    contact_name.short_description = 'Contact Name'

    def email(self, obj):
        return obj.donation.donor.email
    email.short_description = 'Email'

    def mobile_number(self, obj):
        return obj.donation.donor.mobile_number
    mobile_number.short_description = 'Mobile Number'

    def _mark_verified_base(self, req, qs, verified):
        update_cnt = qs.update(verified=verified)
        marked_as = 'verified' if verified else 'unverified'
        msg = "1 item was" if update_cnt == 1 else "%s items were" % update_cnt
        self.message_user(
            req, "%s successfully marked as %s." % (msg, marked_as))

    def mark_verified(self, req, qs):
        self._mark_verified_base(req, qs, True)
    mark_verified.short_description = "Mark as verified"

    def mark_unverified(self, req, qs):
        self._mark_verified_base(req, qs, False)
    mark_unverified.short_description = "Mark as unverified"

    def _mark_base(self, req, qs, status):
        if not req.user.has_perm('app.update_status_item'):
            return self.message_user(
                req,
                PERMISSION_DENIED,
                level=messages.ERROR
            )
        update_cnt = qs.update(status=status.name)
        msg = "1 row was" if update_cnt == 1 else "%s rows were" % update_cnt
        msg = "%s successfully marked as %s." % (msg, status.name)
        self.message_user(req, msg)

    def mark_pledged(self, req, qs):
        self._mark_base(req, qs, ItemStatusEnum.PLEDGED)
    mark_pledged.short_description = "Mark as pledged"

    def mark_received(self, req, qs):
        self._mark_base(req, qs, ItemStatusEnum.RECEIVED)
    mark_received.short_description = "Mark as received"

    def mark_tested(self, req, qs):
        self._mark_base(req, qs, ItemStatusEnum.TESTED)
    mark_tested.short_description = "Mark as tested"

    def mark_refurbished(self, req, qs):
        self._mark_base(req, qs, ItemStatusEnum.REFURBISHED)
    mark_refurbished.short_description = "Mark as refurbished"

    def mark_sold(self, req, qs):
        self._mark_base(req, qs, ItemStatusEnum.SOLD)
    mark_sold.short_description = "Mark as sold"

    def mark_recycled(self, req, qs):
        self._mark_base(req, qs, ItemStatusEnum.RECYCLED)
    mark_recycled.short_description = "Mark as recycled"

    def destroy_item(self, req, qs):
        if not req.user.has_perm('app.destroy_item'):
            return self.message_user(
                req, PERMISSION_DENIED, level=messages.ERROR)

        count, detail = qs.destroy()
        return self.message_user(
            req,
            f"{count} object(s) destroyed. Related detail: {detail}",
            level=messages.SUCCESS
        )
    destroy_item.short_description = "Destroy Item(s)"


class ItemDeviceTypeAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = ('category', 'device_type')
    list_display = ('id', 'category', 'device_type')
    list_filter = ('category',)
    search_fields = ('category', 'device_type')


class ItemDeviceAdmin(admin.ModelAdmin):
    save_on_top = True
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
    search_fields = ('dtype__category', 'dtype__device_type', 'make', 'model')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        kwargs["queryset"] = ItemDeviceType.objects.order_by('category')
        return super(ItemDeviceAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


def _get_readonly_donation_fields(cls, req, obj=None):
    base = cls.readonly_fields
    if not req.user.has_perm('app.update_tax_receipt_created_at'):
        base = base + ('tax_receipt_created_at',)
    return base


def _get_readonly_item_fields(cls, req, obj=None):
    base = cls.readonly_fields
    if not req.user.has_perm('app.update_value_item'):
        base = base + ('value', 'valuation_date', 'valuation_supporting_doc',)
    if not req.user.has_perm('app.update_status_item'):
        base = base + ('status',)
    return base


admin.site.register(Donor, DonorAdmin)
admin.site.register(Donation, DonationAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemDeviceType, ItemDeviceTypeAdmin)
admin.site.register(ItemDevice, ItemDeviceAdmin)
