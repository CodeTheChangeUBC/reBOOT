# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-30 07:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20190730_0312'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={
                'permissions': (
                    ('update_status',
                     'Can update item status'),
                    ('update_value',
                     'Can update item value'))},
        ),
    ]
