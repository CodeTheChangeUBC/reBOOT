# -*- coding: utf-8 -*-

import csv
import tempfile

from django.test import TestCase

from app.models.donor import Donor
from app.worker.tasks import importers


class InitTestCase(TestCase):
    def setUp(self) -> None:

        return super().setUp()

    def test_webform_data_importer(self) -> None:
        with tempfile.TemporaryFile(mode="w+", newline="") as csvfile:
            fieldnames = [
                "Tax Receipt Required",
                "Business Name (if applicable)",
                "Contact Name (First)",
                "Contact Name (Middle)",
                "Contact Name (Last)",
                "Email Address",
                "Phone Number",
                "Address (Street Address)",
                "Address (Address Line 2)",
                "Address (City)",
                "Address (State / Province)",
                "Address (ZIP / Postal Code)",
                "Entry Date",
                "Notes: (parking, buzzer, dock availability, stairs, etc.)",
                "Images or Inventory List",
                "Do you require a certificate of data erasure?",
                "1"]
            writer = csv.DictWriter(f=csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                "Tax Receipt Required": True,
                "Business Name (if applicable)": "Example Co.",
                "Contact Name (First)": "Example",
                "Contact Name (Middle)": "Danger",
                "Contact Name (Last)": "Donor",
                "Email Address": "donor@example.com",
                "Phone Number": "1-234-567-8901",
                "Address (Street Address)": "123 Fake Street",
                "Address (Address Line 2)": "Unit A",
                "Address (City)": "Springfield",
                "Address (State / Province)": "AB",
                "Address (ZIP / Postal Code)": "A1B 2C3",
                "Entry Date": "2023-09-30",
                "Notes: (parking, buzzer, dock availability, stairs, etc.)":
                "Notable quotables",
                "Images or Inventory List": "https://example.com/",
                "Do you require a certificate of data erasure?": "No",
                "1": "Receiver"
            })
            csvfile.seek(0)

            importers.webform_data_importer(
                csvpath=csvfile)

            got_donor = Donor.objects.get(donor_name="Example Co.")

            self.assertIsNotNone(obj=got_donor)
