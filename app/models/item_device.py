from django.db import models
from django.utils import timezone


class ItemDevice(models.Model):
    created_at = models.DateTimeField(default=timezone.localtime)
    updated_at = models.DateTimeField(auto_now=True)

    make = models.CharField('Make', blank=True, max_length=255)
    model = models.CharField('Model', blank=True, max_length=255)
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
