# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.test import Client, TestCase

from app.models.donation import Donation
from app.models.donor import Donor
from app.models.item import Item
from app.models.item_device import ItemDevice


class DataViewTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        user_password = "testing"
        self.user = User.objects.create_superuser(
            "tester", email="tester@example.com", password=user_password)
        self.client.login(username=self.user.username, password=user_password)

        return super().setUp()

    def test_aggregate_value(self) -> None:
        donor = Donor.objects.create()
        donation = Donation.objects.create(donor=donor)
        item_device = ItemDevice.objects.create()
        Item.objects.create(donation=donation, device=item_device,
                            quantity=2, working=True, value=123)

        response = self.client.get(path="/api/value")
        response_json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json["result"][0]["total_value"], 246.0)
