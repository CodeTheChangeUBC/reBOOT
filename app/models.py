# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from datetime import date
from app.resource_model import ResourceModel
from app.constants import donor, item


UNCHANGEABLE_ERROR = 'This instance may not be modified further since the related tax receipt was generated.'


class Donor(ResourceModel):
    donor_name = models.CharField(max_length=75, verbose_name='Donor Name')
    email = models.EmailField(verbose_name='E-mail')
    want_receipt = models.BooleanField(verbose_name='Tax receipt?')
    telephone_number = models.CharField(
        max_length=30, blank=True, verbose_name='Telephone #')
    mobile_number = models.CharField(
        max_length=30, blank=True, verbose_name='Mobile #')
    address_line = models.CharField(
        max_length=256, verbose_name='Street Address')
    city = models.CharField(max_length=30, verbose_name='City')
    province = models.CharField(
        max_length=20, choices=donor.PROVINCE, verbose_name='Province')
    postal_code = models.CharField(max_length=10, verbose_name='Postal Code')
    customer_ref = models.CharField(
        max_length=20, blank=True, verbose_name='Customer Ref.')
    verified = models.BooleanField(
        verbose_name='D & I Verified?', default=False)

    def save(self, *args, **kwargs):
        donations = Donation.objects.select_related().filter(donor__id=self.pk)
        donation_verified, item_verified = True, True
        items = []

        for donation in donations:
            if not donation.verified:
                donation_verified = False
                receipt_number = donation.tax_receipt_no
                items = Item.objects.select_related().filter(donation=receipt_number)

        for item in items:
            if not item.verified:
                item_verified = False

        self.verified = item_verified and donation_verified
        super(Donor, self).save(*args, **kwargs)

    def __unicode__(self):
        return str(self.pk)  # Changed to PK because donation_id was removed


class Donation(ResourceModel):
    donor = models.ForeignKey(
        Donor, on_delete=models.CASCADE, verbose_name='Donor ID')
    tax_receipt_no = models.CharField(
        max_length=9, primary_key=True, verbose_name='Tax Receipt Number')
    tax_receipt_created_at = models.DateTimeField(null=True)
    donate_date = models.DateField('Date Donated')
    pick_up = models.CharField(
        max_length=30, verbose_name='Pick-Up Postal', blank=True)
    verified = models.BooleanField(verbose_name='Verified Donation')

    def __unicode__(self):
        return str(self.tax_receipt_no)

    def allowed_changes(self):
        return self.tax_receipt_created_at is None

    def clean(self):
        if not self.allowed_changes():
            raise ValidationError(UNCHANGEABLE_ERROR)

    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.tax_receipt_no:
            self.tax_receipt_no = gen_tax_receipt_no()
        super(Donation, self).save(*args, **kwargs)

    class Meta:
        permissions = (("generate_tax_receipt", "Can generate tax receipts"),)


class Item(ResourceModel):
    donation = models.ForeignKey(
        Donation, on_delete=models.CASCADE, verbose_name='Tax Receipt Number')
    description = models.CharField(
        max_length=500, choices=item.ITEM_TYPE, verbose_name='Description')
    particulars = models.CharField(
        max_length=500, blank=True, verbose_name='Particulars')
    manufacturer = models.CharField(
        max_length=500, blank=True, verbose_name='Manufacturer')
    model = models.CharField(max_length=50, blank=True, verbose_name='Model')
    quantity = models.IntegerField(verbose_name='Quantity')
    working = models.BooleanField(verbose_name='Is the item working?')
    condition = models.CharField(
        max_length=20, blank=True, verbose_name='Condition')
    quality = models.CharField(
        max_length=20, choices=item.QUALITY, verbose_name='Quality')
    batch = models.CharField(max_length=20, blank=True, verbose_name='Batch')
    value = models.DecimalField(
        max_digits=10, blank=True, decimal_places=2, verbose_name='Value', default=0)
    verified = models.BooleanField(verbose_name='Verified Item', default=False)
    status = models.CharField(
        max_length=20, blank=True, verbose_name='Status', default='received')

    def __unicode__(self):
        return str(self.id)

    def allowed_changes(self):
        return self.donation.tax_receipt_created_at is None

    def clean(self):
        if not self.allowed_changes():
            raise ValidationError(UNCHANGEABLE_ERROR)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Item, self).save(*args, **kwargs)


'''
Private Method
'''


def gen_tax_receipt_no():
    donation = Donation.all_objects.values('tax_receipt_no').order_by().last()
    tax_receipt_no = '0000' if donation is None else donation['tax_receipt_no'][5:]
    tax_receipt_no = int(tax_receipt_no) + 1
    return '%04d-%04d' % (date.today().year, tax_receipt_no)
