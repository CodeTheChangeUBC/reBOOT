# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-05-07 00:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20180502_2007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donor',
            name='province',
            field=models.CharField(choices=[(b'AB', b'Alberta'), (b'BC', b'British Columbia'), (b'ON', b'Ontario'), (b'NS', b'Nova Scotia'), (b'NL', b'Newfoundland and Labrador'), (b'SK', b'Saskatchewan'), (b'YT', b'Yukon'), (b'MB', b'Manitoba'), (b'NU', b'Nunavut'), (b'PE', b'Prince Edward Island'), (b'NT', b'Northwest Territories'), (b'QC', b'Quebec'), (b'NB', b'New Brunswick')], max_length=20, verbose_name='Province'),
        ),
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.CharField(choices=[(b'LCD Monitor', b'LCD Monitor'), (b'Camera', b'Camera'), (b'Playstation', b'Playstation'), (b'Mice', b'Mice'), (b'Fan', b'Fan'), (b'Other Storage Device', b'Other Storage Device'), (b'Audio Receiver', b'Audio Receiver'), (b'Tablet', b'Tablet'), (b'Other gaming console', b'Gaming console'), (b'Other', b'Other'), (b'CPU', b'CPU'), (b'AllInOne Printer', b'All-In-One Printer'), (b'Other Network Device', b'Other Network Device'), (b'CCTV Camera', b'CCTV camera'), (b'TV', b'Television'), (b'DSLR', b'DSLR'), (b'PC-DESKTOP', b'Computer Desktop'), (b'HeatSink', b'Heat Sink'), (b'LED Monitor', b'LED Monitor'), (b'Xbox', b'Xbox'), (b'SSD', b'Solid State Drive'), (b'Inkjet Printer', b'Inkjet Printer'), (b'Speaker', b'Speaker'), (b'RAM', b'Ram'), (b'GPU', b'Video Card'), (b'Cables', b'Cables/Connectors'), (b'HDD', b'Hard Disk Drive'), (b'Router', b'Router'), (b'PSU', b'Power Supply'), (b'Floppy Drive', b'Floppy Diskette'), (b'Other Printer', b'Other Printer'), (b'Switch', b'Network Switch'), (b'Other Monitor', b'Other Monitor'), (b'Mobile Phone', b'Mobile Phone'), (b'PC-Laptop', b'Computer Laptop'), (b'Laser Printer', b'Laser Printer'), (b'Keyboard', b'Keyboard'), (b'Webcam', b'Webcam'), (b'HeadPhone', b'Headphones'), (b'MotherBoard', b'MotherBoard'), (b'LiquidCooler', b'Liquid Cooler'), (b'Server', b'Server'), (b'3d Printer', b'3d Printer'), (b'Mic', b'Microphone')], max_length=500, verbose_name='Description'),
        ),
    ]
