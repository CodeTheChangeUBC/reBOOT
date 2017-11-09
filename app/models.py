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
    # donor_id = models.AutoField(primary_key=True, verbose_name="Donor ID") automatically done by django
    donor_name = models.CharField(max_length=75, verbose_name="Donor Name")
    email = models.EmailField(verbose_name="E-mail")
    want_receipt = models.BooleanField(verbose_name="Tax receipt?")
    telephone_number = models.CharField(validators=[phone_regex], max_length=12, blank=True, verbose_name="Telephone #")
    mobile_number = models.CharField(validators=[phone_regex], max_length=12, blank=True, verbose_name="Mobile #")
    address_line = models.CharField(max_length=500, verbose_name="Street Address")
    city = models.CharField(max_length=30, verbose_name="City")
    province = models.CharField(max_length=20, choices=PROVINCE, verbose_name="Province")
    postal_code = models.CharField(max_length=6, verbose_name="Postal Code")
    verified = models.BooleanField(verbose_name="Donation & Items Verified?", default=False)





    def save(self, *args, **kwargs):

        donations_list = Donation.objects.filter(donor_id=self.pk)
        donationtrue = True
        itemtrue = True

        for donation in donations_list:
            if (donation.verified == False):
                donationtrue = False

            recepitnumber = donation.tax_receipt_no
            item_list = Item.objects.filter(tax_receipt_no=recepitnumber)

            for item in item_list:
                if (item.verified == False):
                    itemtrue = False
                    self.verified = False
                    super(Donor, self).save(*args, **kwargs)

        if(itemtrue and donationtrue):
            self.verified = True
            super(Donor, self).save(*args, **kwargs)
        else:
            self.verified = False
            super(Donor, self).save(*args, **kwargs)






    def __unicode__(self):
        return str(self.pk) #Changed to PK because donation_id was removed
    # To check if the 3 values form a unique combination


#    class meta:
#       unique_together = (('first_name', 'last_name', 'email'), ('address_line1', 'address_line2', 'city', 'postal_code'))


class Donation(models.Model):
    donor_id = models.ForeignKey(Donor, on_delete=models.CASCADE, verbose_name="Donor ID")
    tax_receipt_no = models.CharField(max_length=9, primary_key=True, verbose_name="Tax Receipt Number")
    donate_date = models.DateField('Date Donated')
    donor_city = models.CharField(max_length=50, verbose_name="Donor's City")
    verified = models.BooleanField(verbose_name="Verified Donation", default=False)

    def __unicode__(self):
        return str(self.tax_receipt_no) #Changed to donor_id

class Item(models.Model):
    QUALITY = {
        ('1', 'Very poor'),
        ('2', 'Poor'),
        ('3', 'Average'),
        ('4', 'Good'),
        ('5', 'Excellent')
    }
    tax_receipt_no = models.ForeignKey(Donation, on_delete=models.CASCADE, verbose_name="Tax Receipt Number")
    # item_id = models.AutoField(primary_key=True, verbose_name="Item ID") automatically done by django
    description = models.CharField(max_length=500, blank=True, verbose_name="Description")
    manufacturer = models.CharField(max_length=500, blank=True, verbose_name="Manufacturer")
    model = models.CharField(max_length=50, blank=True, verbose_name="Model")
    quantity = models.IntegerField(verbose_name="Quantity")
    working = models.BooleanField(verbose_name="Is the item working?")  # Slight change here from char to boolean
    condition = models.CharField(max_length=500, blank=True, verbose_name="Condition")
    quality = models.CharField(max_length=20, choices=QUALITY, verbose_name="Quality")
    # Strange property
    batch = models.IntegerField(blank=True, verbose_name="Batch")
    value = models.DecimalField(max_digits=10, blank=True, decimal_places=2, verbose_name="Value")
    verified = models.BooleanField(verbose_name="Verified Item", default = False)
