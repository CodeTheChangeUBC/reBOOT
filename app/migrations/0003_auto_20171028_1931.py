# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-29 02:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20171028_1921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='verified',
            field=models.BooleanField(default=False, verbose_name='Verified Donation'),
        ),
        migrations.AlterField(
            model_name='item',
            name='verified_by_reboot',
            field=models.BooleanField(verbose_name='Verified Item'),
        ),
    ]
