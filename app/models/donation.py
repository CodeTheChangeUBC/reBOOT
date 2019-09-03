from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from app.constants.str import UNCHANGEABLE_ERROR
from app.enums import SourceEnum, DonationStatusEnum
from .resource_model import ResourceModel


def gen_tax_receipt_no():
    d = Donation.all_objects.values('tax_receipt_no').order_by().last()
    if d is None or d['tax_receipt_no'][:4] != str(timezone.localdate().year):
        tax_receipt_no = '0000'
    else:
        tax_receipt_no = d['tax_receipt_no'][5:]
    tax_receipt_no = int(tax_receipt_no) + 1
    return '%04d-%04d' % (timezone.localdate().year, tax_receipt_no)


class Donation(ResourceModel):
    donor = models.ForeignKey('Donor', on_delete=models.CASCADE)
    tax_receipt_no = models.CharField(
        'Donation Number',
        max_length=9,
        primary_key=True,
        default=gen_tax_receipt_no)
    tax_receipt_created_at = models.DateTimeField(
        null=True, default=None, blank=True)
    pledge_date = models.DateField('Pledge Date', default=timezone.now)
    donate_date = models.DateField('Receiving Date', null=True, blank=True)
    pick_up = models.CharField(
        'Pick Up Postal Code', blank=True, max_length=30)
    status = models.CharField(
        'Status',
        max_length=255,
        choices=DonationStatusEnum.choices(),
        default=DonationStatusEnum.default())
    source = models.CharField(
        'Source',
        choices=SourceEnum.choices(),
        default=SourceEnum.default(),
        max_length=255)

    def verified_prop(self):
        return all(self.item_set.values_list('verified', flat=True))
    verified_prop.short_description = 'Verified?'
    verified = property(verified_prop)

    def evaluated_prop(self):
        return all(self.item_set.values_list('valuation_date', flat=True))
    evaluated_prop.short_description = 'Evaluated?'
    evaluated = property(evaluated_prop)

    def __str__(self):
        return str(self.tax_receipt_no)

    def allowed_changes(self):
        return self.tax_receipt_created_at is None

    def clean(self):
        if not self.allowed_changes():
            raise ValidationError(UNCHANGEABLE_ERROR)

    def save(self, *args, **kwargs):
        if not self.tax_receipt_no:
            self.tax_receipt_no = gen_tax_receipt_no()
        super(Donation, self).save(*args, **kwargs)

    class Meta:
        permissions = (('generate_tax_receipt', 'Can generate tax receipts'),)
