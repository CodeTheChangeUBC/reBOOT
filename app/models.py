# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.core.validators import RegexValidator
import simplejson as json
import datetime


# Create your models here.
class Donor(models.Model):
    PROVINCE = {
        ('AB', 'Alberta'),
        ('BC', 'British Columbia'),
        ('SK', 'Saskatchewan'),
        ('MB', 'Manitoba'),
        ('ON', 'Ontario'),
        ('QC', 'Quebec'),
        ('PE', 'Prince Edward Island'),
        ('NS', 'Nova Scotia'),
        ('NL', 'Newfoundland and Labrador'),
        ('NB', 'New Brunswick'),
        ('NT', 'Northwest Territories'),
        ('NU', 'Nunavut'),
        ('YT', 'Yukon')
    }
    # phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
    # message = ('Phone number must be entered in the format: '+999999999'. Up
    # to 15 digits allowed.'))
    donor_name = models.CharField(max_length=75, verbose_name='Donor Name')
    email = models.EmailField(verbose_name='E-mail')
    want_receipt = models.BooleanField(verbose_name='Tax receipt?')
    telephone_number = models.CharField(
        max_length=30, blank=True, verbose_name='Telephone #')
    mobile_number = models.CharField(
        max_length=30, blank=True, verbose_name='Mobile #')
    # telephone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True, verbose_name='Telephone #')
    # mobile_number = models.CharField(validators=[phone_regex],
    # max_length=15, blank=True, verbose_name='Mobile #')
    address_line = models.CharField(
        max_length=256, verbose_name='Street Address')
    city = models.CharField(max_length=30, verbose_name='City')
    province = models.CharField(
        max_length=20, choices=PROVINCE, verbose_name='Province')
    postal_code = models.CharField(max_length=7, verbose_name='Postal Code')
    customer_ref = models.CharField(
        max_length=20, blank=True, verbose_name='Customer Ref.')
    verified = models.BooleanField(
        verbose_name='D & I Verified?', default=False)

    def save(self, *args, **kwargs):
        donations_list = Donation.objects.select_related().filter(donor_id=self.pk)
        donationtrue, itemtrue = True, True
        item_list = []

        for donation in donations_list:
            if not donation.verified:
                donationtrue = False
                receiptnumber = donation.tax_receipt_no
                item_list = Item.objects.select_related().filter(tax_receipt_no=receiptnumber)

        for item in item_list:
            if not item.verified:
                itemtrue = False

        self.verified = itemtrue and donationtrue
        super(Donor, self).save(*args, **kwargs)

    def __unicode__(self):
        return str(self.pk)  # Changed to PK because donation_id was removed

    def serialize(self):
        donor_dict = self.__dict__
        donor_dict.pop("_state")
        json_str = json.dumps(donor_dict)
        return json.loads(json_str)


class Donation(models.Model):
    donor_id = models.ForeignKey(
        Donor, on_delete=models.CASCADE, verbose_name='Donor ID')
    tax_receipt_no = models.CharField(
        max_length=9, primary_key=True, verbose_name='Tax Receipt Number')
    donate_date = models.DateField('Date Donated')
    pick_up = models.CharField(
        max_length=30, verbose_name='Pick-Up Postal', blank=True)
    verified = models.BooleanField(verbose_name='Verified Donation')

    def __unicode__(self):
        return str(self.tax_receipt_no)

    def serialize(self):
        donation_dict = self.__dict__
        if '_state' in donation_dict:
            donation_dict.pop('_state')
        json_str = json.dumps(donation_dict, default=json_serial)
        return json.loads(json_str)


class Item(models.Model):
    QUALITY = {
        ('H', 'High'),
        ('M', 'Medium'),
        ('L', 'Low'),
    }
    tax_receipt_no = models.ForeignKey(
        Donation, on_delete=models.CASCADE, verbose_name='Tax Receipt Number')
    description = models.CharField(
        max_length=500, blank=True, verbose_name='Description')
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
        max_length=20, choices=QUALITY, verbose_name='Quality')
    batch = models.CharField(max_length=20, blank=True, verbose_name='Batch')
    value = models.DecimalField(
        max_digits=10, blank=True, decimal_places=2, verbose_name='Value', default=0)
    verified = models.BooleanField(verbose_name='Verified Item', default=False)

    def __unicode__(self):
        return str(self.id)

    def serialize(self):
        item_dict = self.__dict__
        if '_state' in item_dict:
            item_dict.pop('_state')
        json_str = json.dumps(item_dict, default=json_serial)
        return json.loads(json_str)


'''
Private Method
'''


def json_serial(obj):
        """JSON serializer for objects not serializable by default json code"""

        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        if isinstance(obj, Donor):
            return obj.id
        if isinstance(obj, Donation):
            return obj.tax_receipt_no
        raise TypeError ("Type %s not serializable" % type(obj))