from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from app.constants.str import UNCHANGEABLE_ERROR, DONATION_EVENT_ORDER_ERROR
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
    pledge_date = models.DateField('Pledge Date', default=timezone.now)
    donate_date = models.DateField('Receiving Date', null=True, blank=True)
    test_date = models.DateField('Test Date', null=True, blank=True)
    valuation_date = models.DateField('Valuation Date', null=True, blank=True)
    tax_receipt_created_at = models.DateTimeField(
        'Receipted Date', null=True, default=None, blank=True)
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

    def status_prop(self):
        if self.tax_receipt_created_at:
            return DonationStatusEnum.RECEIPTED.value
        elif self.valuation_date:
            return DonationStatusEnum.EVALED.value
        elif self.test_date:
            return DonationStatusEnum.TESTED.value
        elif self.donate_date:
            return DonationStatusEnum.RECEIVED.value
        else:
            return DonationStatusEnum.OPENED.value
    status_prop.short_description = 'Status'
    status = property(status_prop)

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

    def check_event_order(self):
        """events must happen in this order:

        pledged, received (donated), test, valuation, receipted
        """
        return not (
            (self.donate_date and not self.pledge_date) or
            (self.test_date and not self.donate_date) or
            (self.valuation_date and not self.test_date)
        )

    def check_not_receipted(self):
        """check if donation receipted."""
        return self.tax_receipt_created_at is None

    def clean(self):
        if not self.check_not_receipted():
            raise ValidationError(UNCHANGEABLE_ERROR)
        if not self.check_event_order():
            raise ValidationError(DONATION_EVENT_ORDER_ERROR)

    def save(self, *args, **kwargs):
        if not self.tax_receipt_no:
            self.tax_receipt_no = gen_tax_receipt_no()
        super(Donation, self).save(*args, **kwargs)

    class Meta:
        permissions = (('generate_tax_receipt', 'Can generate tax receipts'),)
