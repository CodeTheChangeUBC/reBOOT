# -*- coding: utf-8 -*-

from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory, TestCase

from app.admin import DonorAdmin
from app.models.donation import Donation
from app.models.donor import Donor
from app.models.item import Item
from app.models.item_device import ItemDevice


class DonorAdminTestCase(TestCase):
    def setUp(self) -> None:
        self.donor = Donor.objects.create(donor_name="Test")

        admin_site = AdminSite()
        self.donor_admin = DonorAdmin(model=Donor, admin_site=admin_site)

        self.request_factory = RequestFactory()

        self.user = User.objects.create_superuser(
            "tester", email="tester@example.com", password="testing")

        return super().setUp()

    def test_donation_count(self) -> None:
        Donation.objects.create(donor=self.donor)

        count = self.donor_admin.donation_count(self.donor)

        self.assertEqual(first=count, second=1)

    def test_item_count(self) -> None:
        donation = Donation.objects.create(donor=self.donor)
        item_device = ItemDevice.objects.create()
        Item.objects.create(donation=donation,
                            device=item_device, quantity=1, working=True)

        count = self.donor_admin.item_count(self.donor)

        self.assertEqual(first=count, second=1)

    def test_destroy_donor(self) -> None:
        request = self.request_factory.delete("")
        request.user = self.user
        sessionMiddleware = SessionMiddleware()
        sessionMiddleware.process_request(request)
        messageMiddleware = MessageMiddleware()
        messageMiddleware.process_request(request)
        donors = Donor.objects.all()
        self.donor_admin.destroy_donor(req=request, qs=donors)

        try:
            gotDonor = Donor.objects.get(donor_name=self.donor.donor_name)
        except Donor.DoesNotExist:
            gotDonor = None

        self.assertIsNone(obj=gotDonor)
