# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.core.validators import RegexValidator


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
    phone_regex = RegexValidator(regex=r'^\+?1?\d{10,12}$',
                                 message="Please enter Number in format: '+1112223333'.")
    donation_id = models.IntegerField(primary_key=True, verbose_name="Donation ID")
    receipt_id = models.CharField(max_length=9, verbose_name="Tax Receipt Number")
    donate_date = models.DateField('Date Donated')
    first_name = models.CharField(max_length=75, verbose_name="First Name")
    last_name = models.CharField(max_length=75, verbose_name="Last Name")
    email = models.EmailField(verbose_name="E-mail")
    want_receipt = models.BooleanField(verbose_name="Tax receipt?")
    business = models.CharField(max_length=100, blank=True, verbose_name="Name of Business/Organisation")
    telephone_number = models.CharField(validators=[phone_regex], max_length=12, blank=True, verbose_name="Phone")
    mobile_number = models.CharField(validators=[phone_regex], max_length=12, blank=True, verbose_name="Phone")
    address_line1 = models.CharField(max_length=100, verbose_name="Street Address - Line 1")
    address_line2 = models.CharField(max_length=100, verbose_name="Street Address - Line 2")
    city = models.CharField(max_length=30, verbose_name="City")
    province = models.CharField(max_length=20, choices=PROVINCE, verbose_name="Province")
    postal_code = models.CharField(max_length=6, verbose_name="Postal Code")


    # To check if the 3 values form a unique combination


#    class meta:
#       unique_together = (('first_name', 'last_name', 'email'), ('address_line1', 'address_line2', 'city', 'postal_code'))


class Donation(models.Model):
    donation_id = models.ForeignKey(Donor, on_delete=models.CASCADE, verbose_name="Donation ID")
    tax_receipt_no = models.CharField(max_length=9, primary_key=True, verbose_name="Tax Receipt Number")
    donate_date = models.DateField('Date Donated')
    donor_city = models.CharField(max_length=50, verbose_name="Donor's City")


class Item(models.Model):
    QUALITY = {
        ('1', 'Very poor'),
        ('2', 'Poor'),
        ('3', 'Average'),
        ('4', 'Good'),
        ('5', 'Excellent')
    }
    tax_receipt_no = models.ForeignKey(Donation, on_delete=models.CASCADE, verbose_name="Tax Receipt Number")
    item_id = models.IntegerField(primary_key=True, verbose_name="Item ID")
    description = models.CharField(max_length=500, blank=True, verbose_name="Description")
    manufacturer = models.CharField(max_length=500, blank=True, verbose_name="Manufacturer")
    model = models.CharField(max_length=50, blank=True, verbose_name="Model")
    quantity = models.IntegerField(verbose_name="Quantity")
    working = models.BooleanField(verbose_name="Is the item working?")  # Slight change here from char to boolean
    condition = models.CharField(max_length=500, blank=True, verbose_name="Condition")
    quality = models.CharField(max_length=20, choices=QUALITY, verbose_name="Quality")
    batch = models.IntegerField(blank=True, verbose_name="Batch")
    value = models.DecimalField(max_digits=10, blank=True, decimal_places=2, verbose_name="Value")
    verified_by_reboot = models.BooleanField(verbose_name="Verified by reBoot?") #Changed to Boolean
