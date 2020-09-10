from django.db import models
from django.core.validators import ValidationError

from app.constants.str import UNCHANGEABLE_ERROR
from app.enums import QualityEnum, ConditionEnum, ItemStatusEnum
from .resource_model import ResourceModel


class Item(ResourceModel):
    donation = models.ForeignKey('Donation', on_delete=models.CASCADE)
    device = models.ForeignKey('ItemDevice', on_delete=models.PROTECT)
    serial_number = models.CharField(
        'Serial Number', blank=True, max_length=255)
    asset_tag = models.CharField('Asset Tag', blank=True, max_length=255)
    particulars = models.CharField('Particulars', max_length=1024, blank=True)
    quantity = models.IntegerField('Quantity')
    working = models.BooleanField('Is Working?', max_length=255)
    condition = models.CharField(
        'Condition',
        blank=True,
        max_length=255,
        choices=ConditionEnum.choices())
    quality = models.CharField(
        'Quality', choices=QualityEnum.choices(), max_length=255, blank=True)
    batch = models.CharField('Batch', blank=True, max_length=255)
    value = models.DecimalField(
        'Value per Item',
        max_digits=10,
        blank=True,
        decimal_places=2,
        default=0)
    verified = models.BooleanField('Verified?', default=False)
    status = models.CharField(
        'Status',
        max_length=255,
        choices=ItemStatusEnum.choices(),
        default=ItemStatusEnum.default())
    weight = models.CharField('Weight', blank=True, null=True, max_length=255)
    valuation_date = models.DateField('Valuation Date', blank=True, null=True)
    valuation_supporting_doc = models.TextField(
        'Valuation Support Doc', blank=True, null=True)
    notes = models.TextField('Notes', blank=True, null=True)

    def particulars_trimmed(self):
        return self.particulars.replace("\r", "").replace("\n", "; ")[:18]
    particulars_trimmed.short_description = 'Particulars Trimmed'

    def __str__(self):
        return str(self.id)

    def allowed_changes(self):
        return self.donation.tax_receipt_created_at is None

    def clean(self):
        if not self.allowed_changes():
            raise ValidationError(UNCHANGEABLE_ERROR)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Item, self).save(*args, **kwargs)

    def total_value(self):
        return format(self.value * self.quantity, '.2f')

    def csv_dict(self):
        return {
            "Quality - Item": self.quantity,
            "Serial Number - Item": self.serial_number,
            "Asset Tag - Item": self.asset_tag,
            "Particulars - Item": self.particulars,
            "Quantity - Item": self.quantity,
            "Working - Item": self.working,
            "Condition - Item": self.condition,
            "Batch - Item": self.batch,
            "Value - Item": self.value,
            "Verified - Item": self.verified,
            "Status - Item": self.status,
            "Weight - Item": self.weight,
            "Valuation Date - Item": self.valuation_date,
            "Valuation Supporting Doc - Item": self.valuation_supporting_doc,
            "Notes - Item": self.notes,
        }

    class Meta:
        permissions = (('update_status_item', 'Can update item status'),
                       ('update_value_item', 'Can update item value'),)
