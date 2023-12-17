# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-08-05 02:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20190802_0933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='condition',
            field=models.CharField(
                blank=True,
                choices=[
                    ('E',
                     'Excellent'),
                    ('G',
                     'Good'),
                    ('F',
                     'Fair'),
                    ('P',
                     'Poor')],
                max_length=255,
                verbose_name='Condition'),
        ),
    ]
