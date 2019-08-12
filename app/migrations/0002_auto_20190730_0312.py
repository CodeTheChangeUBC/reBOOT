# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-30 07:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='donate_date',
            field=models.DateField(blank=True, null=True, verbose_name='Receiving Date'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='pledge_date',
            field=models.DateField(verbose_name='Pledge Date'),
            preserve_default=False,
        ),
    ]