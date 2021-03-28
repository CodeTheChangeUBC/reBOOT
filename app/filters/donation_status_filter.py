from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _
from app.enums import DonationStatusEnum


class DonationStatusFilter(SimpleListFilter):
    title = _('Status')
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('opened', DonationStatusEnum.OPENED.value),
            ('received', DonationStatusEnum.RECEIVED.value),
            ('tested', DonationStatusEnum.TESTED.value),
            ('evaled', DonationStatusEnum.EVALED.value),
            ('receipted', DonationStatusEnum.RECEIPTED.value),
        )

    def queryset(self, request, queryset):
        if self.value() == 'receipted':
            return queryset.exclude(tax_receipt_created_at=None)
        elif self.value() == 'evaled':
            return queryset.exclude(
                valuation_date=None).filter(tax_receipt_created_at=None)
        elif self.value() == 'tested':
            return queryset.exclude(test_date=None).filter(valuation_date=None)
        elif self.value() == 'received':
            return queryset.exclude(donate_date=None).filter(test_date=None)
        elif self.value() == 'opened':
            return queryset.filter(donate_date=None)
        return queryset
