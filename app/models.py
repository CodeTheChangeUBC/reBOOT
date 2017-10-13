# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class Form(models.Model):
    receipt_id = models.CharField(max_length=9)
    donate_date = models.DateField('Date Donated')
    donor_name = models.CharField(max_length=50)
    donor_city = models.CharField(max_length=50)
    # More later



class Raw(models.Model):
    donate_date = models.DateField('Date Donated')
    donor_name = models.CharField(max_length=50)
    donor_city = models.CharField(max_length=50)
    # More later
