# -*- coding: utf-8 -*-

import csv
import io

from django.test import TestCase

from app.models.donor import Donor
from app.worker.tasks import importers


class InitTestCase(TestCase):
    def setUp(self) -> None:

        return super().setUp()

    def test_historical_data_importer(self) -> None:
        fieldnames = [
            # Shared fields
            "Date",

            # Donor fields
            "TRV",
            "Postal Code",
            "Donor Name",
            "Email",
            "Telephone",
            "Mobile",
            "Address",
            "Unit",
            "City",
            "Prov.",
            "CustRef",

            # Donation fields
            "TR#",
            "PPC",

            # DeviceType fields
            "Item Description",

            # ItemDevice fields
            "Manufacturer",
            "Model",

            # Item fields
            "Working",
            "Batch",
            "Item Particulars",
            "Qty",
            "Value",
            "Condition",
            "Quality",
        ]

        csvfile = io.StringIO()
        writer = csv.DictWriter(f=csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({
            # Shared fields
            "Date": "2023-10-19",

            # Donor fields
            "TRV": "REFUSED",
            "Postal Code": "A1B 2C3",
            "Donor Name": "Example Danger Donor",
            "Email": "donor@example.com",
            "Telephone": "1-234-567-8901",
            "Mobile": "2-345-678-9012",
            "Address": "123 Fake Street",
            "Unit": "A",
            "City": "Springfield",
            "Prov.": "AB",
            "CustRef": "Buddy",

            # Donation fields
            "TR#": "123",
            "PPC": "Please",

            # Device type fields
            "Item Description": "Thingamajig",

            # ItemDevice fields
            "Manufacturer": "Widget, Co.",
            "Model": "W1",

            # Item fields
            "Working": "Y",
            "Batch": "1",
            "Item Particulars": "It's pretty peculiar",
            "Qty": 6,
            "Value": "123.45",
            "Condition": "G",
            "Quality": "M",
        })
        csvvalue = csvfile.getvalue().splitlines()

        importers.historical_data_importer.apply(args=[csvvalue])

        got_donor = Donor.objects.get(donor_name="Example Danger Donor")

        self.assertIsNotNone(obj=got_donor)
