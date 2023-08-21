# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.test import Client, TestCase

from app.models.donor import Donor


class APIViewsTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        user_password = "testing"
        self.user = User.objects.create_superuser(
            "tester", email="tester@example.com", password=user_password)
        self.client.login(username=self.user.username, password=user_password)

        return super().setUp()

    def test_autocomplete_name(self) -> None:
        want_donor = Donor.objects.create(donor_name="Test Donor")

        response = self.client.get(
            path="/api/autocomplete_name", data={"key": "Test"})
        response_json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json[0]["donorName"], want_donor.donor_name)
