from app.models import Donor
from django.contrib.auth.models import User
from django.core import serializers
from django.test import Client, TestCase


class DonorViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        user_password = "testing"
        self.user = User.objects.create_user(
            "tester", email="tester@example.com", password=user_password
        )
        self.client.login(username=self.user.username, password=user_password)

    def test_get(self):
        donor = Donor(donor_name="Test")
        donor.save()
        response = self.client.get("/api/donor", {"id": donor.id})
        response_json = response.json()

        self.assertEqual(response_json["donorName"], donor.donor_name)
