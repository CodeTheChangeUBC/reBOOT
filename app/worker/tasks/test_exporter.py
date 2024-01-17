# -*- coding: utf-8 -*-

from django.core.serializers import serialize
from django.test import TestCase

from app.models.donation import Donation
from app.models.donor import Donor
from app.models.item import Item
from app.models.item_device import ItemDevice
from app.worker.tasks.exporter import exporter


class ExporterTestCase(TestCase):
    def setUp(self) -> None:
        donor = Donor.objects.create(
            donor_name="Test", contact_name="Best", email="test@example.com",
            mobile_number="+1 (234) 567-8901")
        donation = Donation.objects.create(donor=donor)
        item_device = ItemDevice.objects.create()
        self.item = Item.objects.create(donation=donation,
                                        device=item_device, quantity=1,
                                        working=True)
        return super().setUp()

    def test_exporter(self) -> None:
        file_name = "test_exporter.csv"
        queryset = Item.objects.all()
        qs = serialize(format="json", queryset=queryset)
        total_count = len(queryset)

        result = exporter.apply(args=[file_name, qs, total_count])
        response = result.get()
        content_type = response["Content-Type"]

        self.assertEqual(first=response.status_code, second=200)
        self.assertEqual(first=content_type, second="application/csv")
