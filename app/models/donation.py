from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from functools import reduce

from app.constants.str import UNCHANGEABLE_ERROR, DONATION_EVENT_ORDER_ERROR
from app.enums import SourceEnum, DonationStatusEnum
from .resource_model import ResourceModel


def gen_tax_receipt_no():
    cur_year = timezone.localdate().year
    d = Donation.all_objects.filter(
        tax_receipt_no__istartswith=f'{cur_year}'
    ).order_by('tax_receipt_no').last()
    trn = '0000' if d is None else d.tax_receipt_no[5:]
    return '%04d-%04d' % (cur_year, int(trn) + 1)


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
    source = models.CharField(
        'Source',
        choices=SourceEnum.choices(),
        default=SourceEnum.default(),
        max_length=255)
    notes = models.TextField('Notes', blank=True, null=True)

    def total_value(self):
        quantity_value = self.item_set.values_list('quantity', 'value')
        summed = reduce(lambda a, b: a+b[0]*b[1], quantity_value, 0)
        return "${:.2f}".format(summed)
    total_value.short_description = 'Total Value'

    def status(self):
        curstatus = DonationStatusEnum.OPENED.value
        if self.tax_receipt_created_at:
            curstatus = DonationStatusEnum.RECEIPTED.value
        elif self.valuation_date:
            curstatus = DonationStatusEnum.EVALED.value
        elif self.test_date:
            curstatus = DonationStatusEnum.TESTED.value
        elif self.donate_date:
            curstatus = DonationStatusEnum.RECEIVED.value
        return curstatus
    status.short_description = 'Status'

    def verified(self):
        return all(self.item_set.values_list('verified', flat=True))
    verified.short_description = 'Verified?'
    verified.boolean = True

    def evaluated(self):
        return all(self.item_set.values_list('valuation_date', flat=True))
    evaluated.short_description = 'Evaluated?'
    evaluated.boolean = True

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

    def csv_dict(self):
        return {
            "Tax Receipt Number - Donation": self.tax_receipt_no,
            "Pledge Date - Donation": self.pledge_date,
            "Donate Date - Donation": self.donate_date,
            "Test Date - Donation": self.test_date,
            "Valuation Date - Donation": self.valuation_date,
            "Receipted Date - Donation": self.tax_receipt_created_at,
            "Pick Up Postal Code - Donation": self.pick_up,
            "Source - Donation": self.source,
        }

    def total_quantity_and_value(self):
        total_qty, total_value = 0, 0
        for item in self.item_set.all():
            total_qty += item.quantity
            total_value += float(item.value) * item.quantity
        return total_qty, total_value

    class Meta:
        permissions = (
            ('generate_tax_receipt', 'Can generate tax receipts'),
            ('change_tax_receipt_created_at',
                'Can change tax receipt created at'),)
