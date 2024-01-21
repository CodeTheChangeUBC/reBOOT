# -*- coding: utf-8 -*-

from django.core import serializers
from django.test import TestCase

from app.models.donation import Donation
from app.models.donor import Donor
from app.worker import tasks


class InitTestCase(TestCase):
    def setUp(self) -> None:
        self.donor = Donor.objects.create()

        return super().setUp()

    def test_receiptor_single_file(self) -> None:
        Donation.objects.create(donor=self.donor, donate_date="2023-09-30")
        queryset = Donation.objects.all()
        queryset_json = serializers.serialize(format="json", queryset=queryset)
        total_count = Donation.objects.count()

        result = tasks.receiptor.apply(args=[queryset_json, total_count])
        response = result.get()

        self.assertEqual(first=response.status_code, second=200)
        self.assertEqual(
            first=response['Content-Type'], second="application/pdf")

    def test_receiptor_multiple_files(self) -> None:
        Donation.objects.create(donor=self.donor, donate_date="2023-09-30")
        Donation.objects.create(donor=self.donor, donate_date="2023-10-29")
        queryset = Donation.objects.all()
        queryset_json = serializers.serialize(format="json", queryset=queryset)
        total_count = Donation.objects.count()

        result = tasks.receiptor.apply(args=[queryset_json, total_count])
        response = result.get()

        self.assertEqual(first=response.status_code, second=200)
        self.assertEqual(
            first=response['Content-Type'], second="application/zip")
