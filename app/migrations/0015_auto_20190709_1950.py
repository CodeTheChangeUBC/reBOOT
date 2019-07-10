# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-10 02:50
from __future__ import unicode_literals

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20190613_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='tax_receipt_no',
            field=models.CharField(default=app.models.gen_tax_receipt_no, max_length=9, primary_key=True, serialize=False, verbose_name='Donation Number'),
        ),
    ]