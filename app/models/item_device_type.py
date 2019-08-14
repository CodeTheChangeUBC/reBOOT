from django.db import models
from django.utils import timezone

from app.enums import ItemCategoryEnum
from .resource_model import ResourceModel


class ItemDeviceType(models.Model):
    created_at = models.DateTimeField(default=timezone.localtime)
    updated_at = models.DateTimeField(auto_now=True)

    device_type = models.CharField('Device Type', max_length=255)
    category = models.CharField(
        'Category', max_length=255, choices=ItemCategoryEnum.choices())

    def __str__(self):
        return '%s - %s' % (self.get_category_display(), self.device_type)

    class Meta:
        unique_together = ('device_type', 'category')
