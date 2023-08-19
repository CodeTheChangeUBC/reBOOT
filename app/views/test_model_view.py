from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.utils.http import urlencode

from app.models import Donor


class DonorViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url_path = "/api/donor"

        user_password = "testing"
        self.user = User.objects.create_superuser(
            "tester", email="tester@example.com", password=user_password
        )
        self.client.login(username=self.user.username, password=user_password)

        self.test_donor = Donor.objects.create(donor_name="Test Donor")

    def test_get(self):
        response = self.client.get(self.url_path, {"id": self.test_donor.id})
        response_json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json["donorName"],
                         self.test_donor.donor_name)

    def test_post(self):
        want_donor_name = "Other Test Donor"
        want_email = "other-test-donor@example.com"

        response = self.client.post(
            self.url_path,
            {
                "donorName": want_donor_name,
                "email": want_email,
                "wantReceipt": "true",
                "telephoneNumber": "+1 (234) 576-8901",
                "mobileNumber": "+2 (345) 678-9012",
                "addressLineOne": "123 Fake Street",
                "addressLineTwo": "Unit A",
                "city": "Springfield",
                "province": "Mystery",
                "postalCode": "A1B 2C3",
                "customerRef": "Unknown",
            },
        )
        donor = Donor.objects.get(donor_name=want_donor_name)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(donor.email, want_email)

    def test_put(self):
        want_donor_name = "Best Donor"

        data = urlencode(
            {
                "id": self.test_donor.id,
                "donorName": want_donor_name,
                "email": "test@example.com",
                "wantReceipt": "true",
                "telephoneNumber": "+1 (234) 576-8901",
                "mobileNumber": "+2 (345) 678-9012",
                "addressLineOne": "123 Fake Street",
                "addressLineTwo": "Unit A",
                "city": "Springfield",
                "province": "Mystery",
                "postalCode": "A1B 2C3",
                "customerRef": "Unknown",
            }
        )
        response = self.client.put(
            self.url_path,
            data,
            content_type="application/x-www-form-urlencoded",
        )
        self.test_donor.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.test_donor.donor_name, want_donor_name)

    def test_delete(self):
        data = urlencode({"id": self.test_donor.id})
        response = self.client.delete(self.url_path, data)
        donors = Donor.objects.filter(donor_name=self.test_donor.donor_name)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(donors), 0)
