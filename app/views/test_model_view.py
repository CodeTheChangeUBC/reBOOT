from app.models import Donor
from django.contrib.auth.models import User
from django.test import Client, TestCase


class DonorViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        user_password = "testing"
        self.user = User.objects.create_superuser(
            "tester", email="tester@example.com", password=user_password
        )
        self.client.login(username=self.user.username, password=user_password)

    def test_get(self):
        donor = Donor(donor_name="Test")
        donor.save()
        response = self.client.get("/api/donor", {"id": donor.id})
        response_json = response.json()

        self.assertEqual(response_json["donorName"], donor.donor_name)

    def test_post(self):
        donor_name = "Test"
        email = "test@example.com"
        self.client.post(
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

        self.assertEqual(donor.email, email)
