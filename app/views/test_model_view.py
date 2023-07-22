from app.models import Donor
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.utils.http import urlencode


class DonorViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        user_password = "testing"
        self.user = User.objects.create_superuser(
            "tester", email="tester@example.com", password=user_password
        )
        self.client.login(username=self.user.username, password=user_password)

        self.test_donor_name = "Test Donor"
        Donor.objects.create(donor_name=self.test_donor_name)

    def test_get(self):
        donor = Donor.objects.get(donor_name=self.test_donor_name)
        response = self.client.get("/api/donor", {"id": donor.id})
        response_json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json["donorName"], donor.donor_name)

    def test_post(self):
        donor_name = "Other Test Donor"
        email = "other-test-donor@example.com"
        response = self.client.post(
            "/api/donor",
            {
                "donorName": donor_name,
                "email": email,
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
        donor = Donor.objects.get(donor_name=donor_name)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(donor.email, email)

    def test_put(self):
        donor = Donor.objects.get(donor_name=self.test_donor_name)
        updated_donor_name = "Best Donor"
        data = urlencode(
            {
                "id": donor.id,
                "donorName": updated_donor_name,
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
            "/api/donor",
            data,
            content_type="application/x-www-form-urlencoded",
        )
        donor.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(donor.donor_name, updated_donor_name)

    def test_delete(self):
        donor = Donor.objects.get(donor_name=self.test_donor_name)
        data = urlencode({"id": donor.id})
        response = self.client.delete("/api/donor", data)
        donors = Donor.objects.filter(donor_name=donor.donor_name)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(donors), 0)
