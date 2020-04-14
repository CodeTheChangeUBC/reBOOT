import operator
from django.db import models
from django.db.models import F
from functools import reduce

from app.enums import ProvinceEnum, TaxReceiptViaEnum
from .resource_model import ResourceModel, ResourceManager, ResourceQuerySet


class DonorQuerySet(ResourceQuerySet):
    def _get_orgs(self):
        return self.exclude(contact_name='') \
            .exclude(donor_name=F('contact_name')) \
            .values_list('id', flat=True)

    def are_businesses(self):
        """Return donors that are businesses.

        Individuals are donors with not matching contact_name to
        donor_name
        """
        return self.filter(id__in=self._get_orgs())

    def are_individuals(self):
        """Return donors that are individuals.

        Individuals are donors with empty contact_name or matching
        contact_name
        """
        return self.exclude(id__in=self._get_orgs())


class DonorManager(ResourceManager):
    def get_queryset(self):
        if self.alive_only:
            return DonorQuerySet(self.model).alive()
        return DonorQuerySet(self.model)


class Donor(ResourceModel):
    objects = DonorManager()
    all_objects = DonorManager(alive_only=False)

    donor_name = models.CharField('Donor Name', max_length=255)
    contact_name = models.CharField('Contact Name', blank=True, max_length=255)
    email = models.EmailField('Email')
    want_receipt = models.CharField(
        'Tax Receipt Via',
        choices=TaxReceiptViaEnum.choices(),
        default=TaxReceiptViaEnum.default(),
        max_length=255)
    telephone_number = models.CharField(
        'Telephone #', blank=True, max_length=255)
    mobile_number = models.CharField('Mobile #', blank=True, max_length=255)
    address_line_one = models.CharField(
        'Address Line 1', blank=True, max_length=255)
    address_line_two = models.CharField(
        'Address Line 2', blank=True, max_length=255)
    city = models.CharField('City', max_length=255)
    province = models.CharField(
        'Province', choices=ProvinceEnum.choices(), max_length=255)
    postal_code = models.CharField('Postal Code', max_length=10)
    customer_ref = models.CharField(
        'Customer Ref.', blank=True, max_length=255)

    def verified(self):
        subset = list(map((lambda x: x.verified()), self.donation_set.all()))
        return reduce(operator.and_, subset, True)
    verified.short_description = 'Verified?'
    verified.boolean = True

    def is_org(self):
        return self.contact_name != '' and self.contact_name != self.donor_name

    def save(self, *args, **kwargs):
        if not self.contact_name:
            self.contact_name = self.donor_name
        super(Donor, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.donor_name)

    def csv_dict(self):
        return {
            "Donor Name - Donor": self.donor_name,
            "Contact Name - Donor": self.contact_name,
            "Email - Donor": self.email,
            "Tax Receipt Via - Donor": self.want_receipt,
            "Telephone Number - Donor": self.telephone_number,
            "Address Line 1 - Donor": self.address_line_one,
            "Address Line 2 - Donor": self.address_line_two,
            "City - Donor": self.city,
            "Province - Donor": self.province,
            "Postal Code - Donor": self.postal_code,
            "Customer Reference - Donor": self.customer_ref,
        }
