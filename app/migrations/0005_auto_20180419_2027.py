# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-20 03:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20180330_2201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donor',
            name='province',
            field=models.CharField(choices=[('AB', 'Alberta'), ('BC', 'British Columbia'), ('ON', 'Ontario'), ('NS', 'Nova Scotia'), ('NL', 'Newfoundland and Labrador'), ('SK', 'Saskatchewan'), ('YT', 'Yukon'), ('MB', 'Manitoba'), ('NU', 'Nunavut'), ('PE', 'Prince Edward Island'), ('NT', 'Northwest Territories'), ('QC', 'Quebec'), ('NB', 'New Brunswick')], max_length=20, verbose_name='Province'),
        ),
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.CharField(choices=[('LCD Monitor', 'LCD Monitor'), ('Camera', 'Camera'), ('Playstation', 'Playstation'), ('Mice', 'Mice'), ('Fan', 'Fan'), ('Other Storage Device', 'Other Storage Device'), ('Audio Receiver', 'Audio Receiver'), ('Tablet', 'Tablet'), ('Other gaming console', 'Gaming console'), ('Other', 'Other'), ('CPU', 'CPU'), ('AllInOne Printer', 'All-In-One Printer'), ('Other Network Device', 'Other Network Device'), ('CCTV Camera', 'CCTV camera'), ('TV', 'Television'), ('DSLR', 'DSLR'), ('PC-DESKTOP', 'Computer Desktop'), ('HeatSink', 'Heat Sink'), ('LED Monitor', 'LED Monitor'), ('Xbox', 'Xbox'), ('SSD', 'Solid State Drive'), ('Inkjet Printer', 'Inkjet Printer'), ('Speaker', 'Speaker'), ('RAM', 'Ram'), ('GPU', 'Video Card'), ('Cables', 'Cables/Connectors'), ('HDD', 'Hard Disk Drive'), ('Router', 'Router'), ('PSU', 'Power Supply'), ('Floppy Drive', 'Floppy Diskette'), ('Other Printer', 'Other Printer'), ('Switch', 'Network Switch'), ('Other Monitor', 'Other Monitor'), ('Mobile Phone', 'Mobile Phone'), ('PC-Laptop', 'Computer Laptop'), ('Laser Printer', 'Laser Printer'), ('Keyboard', 'Keyboard'), ('Webcam', 'Webcam'), ('HeadPhone', 'Headphones'), ('MotherBoard', 'MotherBoard'), ('LiquidCooler', 'Liquid Cooler'), ('Server', 'Server'), ('3d Printer', '3d Printer'), ('Mic', 'Microphone')], max_length=500, verbose_name='Description'),
        ),
    ]
