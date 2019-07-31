from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _


class DonorBusinessFilter(SimpleListFilter):
    title = 'business'
    parameter_name = 'is_business'

    def lookups(self, request, model_admin):
        return (
            ('1', _('Yes')),
            ('0', _('No'))
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.are_businesses()
        elif self.value() == '0':
            return queryset.are_individuals()
        return queryset
