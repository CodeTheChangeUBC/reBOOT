from django.db import models
from django.utils import timezone
from app.constants.item_map import ITEM_MAP
from app.enums import ItemCategoryEnum


class ItemDevice(models.Model):
    created_at = models.DateTimeField(default=timezone.localtime)
    updated_at = models.DateTimeField(auto_now=True)

    make = models.CharField('Make', blank=True, max_length=1024)
    model = models.CharField('Model', blank=True, max_length=1024)
    dtype = models.ForeignKey(
        'ItemDeviceType',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Device Type')
    cpu_type = models.CharField(
        'CPU Type', blank=True, max_length=255, null=True)
    speed = models.CharField('Speed', blank=True, max_length=255, null=True)
    memory = models.DecimalField(
        'Memory (MB)', max_digits=10, decimal_places=2, blank=True, null=True)
    hd_size = models.DecimalField(
        'HD Size (GB)', max_digits=10, decimal_places=2, blank=True, null=True)
    screen_size = models.CharField(
        'Screen Size', blank=True, max_length=255, null=True)
    hdd_serial_number = models.CharField(
        'HDD Serial Number', blank=True, max_length=255, null=True)
    operating_system = models.CharField(
        'Operating System', blank=True, max_length=255, null=True)

    def __str__(self):
        if self.make and self.model:
            return '%s (%s)' % (self.model, self.make)
        elif self.make or self.model:
            return '%s%s' % (self.model, self.make)
        else:
            return '-'

    """
    :return: item device dict for csv
    :rtype: dict

    for the device without its type, set it as MISCELLANEOUS
    """
    def csv_dict(self):
        return {
            "Category - Item Device Type": self.dtype.device_type
            if self.dtype is not None else ITEM_MAP.get("")["device_type"],
            "Type - Item Device Type":
            ItemCategoryEnum[self.dtype.category].value
            if self.dtype is not None else ITEM_MAP.get("")["category"],
            "Make - Item Device": self.make,
            "Model - Item Device": self.model,
            "CPU Type - Item Device": self.cpu_type,
            "Speed - Item Device": self.speed,
            "Memory (MB) - Item Device": self.memory,
            "HD SIZE (GB) - Item Device": self.hd_size,
            "Screen Size - Item Device": self.screen_size,
            "HDD Serial Number - Item Device": self.hdd_serial_number,
            "Operating System - Item Device": self.operating_system,
        }
