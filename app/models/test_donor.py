from django.test import TestCase

from app.models import Donor
from django.db.utils import DataError


class DonorTestCase(TestCase):
    def test_complete_arguments(self):
        test_donor = Donor(
            donor_name="Tesla",
            email="NickT@gmail.com",
            want_receipt="Mail",
            telephone_number="604-123-5678",
            mobile_number="604-123-5678",
            address_line_one="Mars street",
            address_line_two="Unit 2",
            city="Tokyo",
            province="Japan",
            postal_code="123123",
        )
        test_donor.save()

        response = Donor.objects.get(donor_name="Tesla")
        self.assertEqual(response.donor_name, "Tesla", "donor_name")
        self.assertEqual(response.email, "NickT@gmail.com", "email")
        self.assertEqual(response.want_receipt, "Mail", "want_receipt")
        self.assertEqual(response.telephone_number, "604-123-5678", "telephone_number")
        self.assertEqual(response.mobile_number, "604-123-5678", "mobile_number")
        self.assertEqual(response.address_line_one, "Mars street", "address_line_one")
        self.assertEqual(response.address_line_two, "Unit 2", "address_line_two")
        self.assertEqual(response.city, "Tokyo", "city")
        self.assertEqual(response.province, "Japan", "province")
        self.assertEqual(response.postal_code, "123123", "postal_code")
        self.assertEqual(response.verified(), True, "verified()")

    def test_invalid_telephone_number(self):
        raised = False

        try:
            # DOES NOT THROW ANYTHING.
            test_donor = Donor(
                donor_name="Zavala",
                telephone_number="111122223333123",
                want_receipt=False,
            )
            test_donor.save()
        except:
            raised = True

        self.assertFalse(
            raised,
            "Saving a donor with an invalid telephone number should not raise an exception",
        )

    def test_default_want_receipt(self):
        test_donor = Donor(donor_name="Tohru", telephone_number="123-333-3333")
        test_donor.save()

        response = Donor.objects.get(donor_name="Tohru")
        self.assertEqual(response.want_receipt, "EMAIL")

    def test_invalid_postal_code(self):
        with self.assertRaisesRegex(DataError, "value too long"):
            test_donor = Donor(
                donor_name="Kobayashi",
                postal_code="12345678123afasdf",
                want_receipt=False,
            )
            test_donor.save()
