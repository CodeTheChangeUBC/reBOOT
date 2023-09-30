# -*- coding: utf-8 -*-

from django.core import serializers
from django.test import TestCase

from app.models.donation import Donation
from app.models.donor import Donor
from app.worker import tasks


class InitTestCase(TestCase):
    def setUp(self) -> None:

        return super().setUp()

    def test_receiptor(self) -> None:
        donor = Donor.objects.create()
        Donation.objects.create(donor=donor, donate_date="2023-09-30")
        queryset = Donation.objects.all()
        queryset_json = serializers.serialize(format="json", queryset=queryset)
        total_count = Donation.objects.count()

        response = tasks.receiptor(
            queryset=queryset_json, total_count=total_count)

        self.assertEqual(first=response.status_code, second=200)
        self.assertEqual(
            first=response['Content-Type'], second="application/pdf")
