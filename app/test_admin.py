# -*- coding: utf-8 -*-

from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory, TestCase

from app.admin import DonationAdmin, DonorAdmin, ItemAdmin, ItemInline
from app.enums.item_status_enum import ItemStatusEnum
from app.models.donation import Donation
from app.models.donor import Donor
from app.models.item import Item
from app.models.item_device import ItemDevice


class DonorAdminTestCase(TestCase):
    def setUp(self) -> None:
        self.donor = Donor.objects.create(donor_name="Test")

        self.donation = Donation.objects.create(donor=self.donor)

        admin_site = AdminSite()
        self.donor_admin = DonorAdmin(model=Donor, admin_site=admin_site)

        self.request_factory = RequestFactory()

        self.user = User.objects.create_superuser(
            username="tester", email="tester@example.com", password="testing")

        return super().setUp()

    def test_donation_count(self) -> None:
        count = self.donor_admin.donation_count(obj=self.donor)

        self.assertEqual(first=count, second=1)

    def test_item_count(self) -> None:
        item_device = ItemDevice.objects.create()
        Item.objects.create(donation=self.donation,
                            device=item_device, quantity=1, working=True)

        count = self.donor_admin.item_count(obj=self.donor)

        self.assertEqual(first=count, second=1)

    def test_destroy_donor(self) -> None:
        request = self.request_factory.delete(path="")
        request.user = self.user
        sessionMiddleware = SessionMiddleware()
        sessionMiddleware.process_request(request=request)
        messageMiddleware = MessageMiddleware()
        messageMiddleware.process_request(request=request)
        donors = Donor.objects.all()

        self.donor_admin.destroy_donor(req=request, qs=donors)

        try:
            got_donor = Donor.objects.get(donor_name=self.donor.donor_name)
        except Donor.DoesNotExist:
            got_donor = None

        self.assertIsNone(obj=got_donor)


class ItemInlineTestCase(TestCase):
    def setUp(self) -> None:
        admin_site = AdminSite()
        self.item_inline = ItemInline(
            parent_model=Donation, admin_site=admin_site)

        self.request_factory = RequestFactory()

        self.user = User.objects.create_user(
            username="tester", email="tester@example.com", password="testing")

        return super().setUp()

    def test_get_readonly_fields(self) -> None:
        want_readonly_fields = ("value", "valuation_date",
                                "valuation_supporting_doc", "status")

        request = self.request_factory.patch(path="")
        request.user = self.user

        got_readonly_fields = self.item_inline.get_readonly_fields(req=request)

        self.assertTupleEqual(tuple1=got_readonly_fields,
                              tuple2=want_readonly_fields)


class DonationAdminTestCase(TestCase):
    def setUp(self) -> None:
        self.donor = Donor.objects.create(
            donor_name="Test", contact_name="Best", email="test@example.com",
            mobile_number="+1 (234) 567-8901")

        self.donation = Donation.objects.create(donor=self.donor)
        item_device = ItemDevice.objects.create()
        Item.objects.create(donation=self.donation,
                            device=item_device, quantity=1, working=True)

        admin_site = AdminSite()
        admin_site.register(model_or_iterable=Donor)
        self.donation_admin = DonationAdmin(
            model=Donation, admin_site=admin_site)

        self.request_factory = RequestFactory()

        self.user = User.objects.create_superuser(
            username="tester", email="tester@example.com", password="testing")

        return super().setUp()

    def test_donor_id(self) -> None:
        got_donor_id = self.donation_admin.donor_id(obj=self.donation)

        self.assertEqual(first=got_donor_id, second=self.donor.id)

    def test_donor_contact_name(self) -> None:
        got_donor_contact_name = self.donation_admin.donor_contact_name(
            obj=self.donation)

        self.assertEqual(first=got_donor_contact_name,
                         second=self.donor.contact_name)

    def test_donor_donor_name(self) -> None:
        got_donor_donor_name = self.donation_admin.donor_donor_name(
            obj=self.donation)

        self.assertEqual(first=got_donor_donor_name,
                         second=self.donor.donor_name)

    def test_donor_email(self) -> None:
        got_donor_email = self.donation_admin.donor_email(
            obj=self.donation)

        self.assertEqual(first=got_donor_email,
                         second=self.donor.email)

    def test_donor_mobile_number(self) -> None:
        got_donor_mobile_number = self.donation_admin.donor_mobile_number(
            obj=self.donation)

        self.assertEqual(first=got_donor_mobile_number,
                         second=self.donor.mobile_number)

    def test_item_count(self) -> None:
        want_count = len(self.donation.item_set.all())
        got_count = self.donation_admin.item_count(obj=self.donation)

        self.assertEqual(first=got_count, second=want_count)

    def test_mark_items_verified(self) -> None:
        request = self.request_factory.post(path="")
        sessionMiddleware = SessionMiddleware()
        sessionMiddleware.process_request(request=request)
        messageMiddleware = MessageMiddleware()
        messageMiddleware.process_request(request=request)
        donations = Donation.objects.all()

        self.donation_admin.mark_items_verified(req=request, qs=donations)

        verified = self.donation.verified()

        self.assertTrue(expr=verified)

    def test_mark_items_unverified(self) -> None:
        request = self.request_factory.post(path="")
        sessionMiddleware = SessionMiddleware()
        sessionMiddleware.process_request(request=request)
        messageMiddleware = MessageMiddleware()
        messageMiddleware.process_request(request=request)
        donations = Donation.objects.all()

        self.donation.item_set.update(verified=True)
        self.donation_admin.mark_items_unverified(req=request, qs=donations)

        verified = self.donation.verified()

        self.assertFalse(expr=verified)

    def test_generate_receipt(self) -> None:
        self.donation.item_set.update(
            status=ItemStatusEnum.RECEIVED, verified=True,
            valuation_date="2023-09-12")
        self.donation.valuation_date = "2023-09-12"
        self.donation.save()

        request = self.request_factory.post(path="")
        request.user = self.user
        donations = Donation.objects.all()

        response = self.donation_admin.generate_receipt(
            req=request, qs=donations)

        self.assertContains(response=response, text="", status_code=302)

    def test_generate_csv(self) -> None:
        request = self.request_factory.post(path="")
        request.user = self.user
        donations = Donation.objects.all()

        response = self.donation_admin.generate_csv(req=request, qs=donations)

        self.assertContains(response=response, text="", status_code=302)

    def test_destroy_donation(self) -> None:
        request = self.request_factory.delete(path="")
        request.user = self.user
        sessionMiddleware = SessionMiddleware()
        sessionMiddleware.process_request(request=request)
        messageMiddleware = MessageMiddleware()
        messageMiddleware.process_request(request=request)
        donations = Donation.objects.all()

        self.donation_admin.destroy_donation(req=request, qs=donations)

        try:
            got_donation = Donation.objects.get(donor=self.donor)
        except Donation.DoesNotExist:
            got_donation = None

        self.assertIsNone(obj=got_donation)

    def test_response_change_generate_receipt(self) -> None:
        self.donation.item_set.update(
            status=ItemStatusEnum.RECEIVED, verified=True,
            valuation_date="2023-09-12")
        self.donation.valuation_date = "2023-09-12"
        self.donation.save()

        request = self.request_factory.post(
            path="", data={"_generate_receipt": ""})
        request.user = self.user
        sessionMiddleware = SessionMiddleware()
        sessionMiddleware.process_request(request=request)
        messageMiddleware = MessageMiddleware()
        messageMiddleware.process_request(request=request)

        response = self.donation_admin.response_change(
            req=request, obj=self.donation)

        self.assertEqual(first=response.status_code, second=302)

    def test_response_change_mark_items_verified(self) -> None:
        request = self.request_factory.post(
            path="", data={"_mark_items_verified": ""})
        request.user = self.user
        sessionMiddleware = SessionMiddleware()
        sessionMiddleware.process_request(request=request)
        messageMiddleware = MessageMiddleware()
        messageMiddleware.process_request(request=request)

        response = self.donation_admin.response_change(
            req=request, obj=self.donation)

        verified = self.donation.verified()

        self.assertEqual(first=response.status_code, second=302)
        self.assertTrue(expr=verified)

    def test_get_readonly_fields(self) -> None:
        request = self.request_factory.get(path="")
        request.user = self.user

        got_readonly_fields = self.donation_admin.get_readonly_fields(
            req=request, obj=self.donation)

        self.assertSequenceEqual(seq1=got_readonly_fields, seq2=(
            "donor_contact_name", "donor_donor_name", "donor_email",
            "donor_mobile_number", "status"))

    def test_formfield_for_foreignkey(self) -> None:
        request = self.request_factory.get(path="")

        got_formfield = self.donation_admin.formfield_for_foreignkey(
            db_field=Donation._meta.get_field(field_name="donor"), request=request, using=None)
        got_widget_context = got_formfield.widget.get_context(name=None, value=None, attrs=None)
        got_related_add_url = got_widget_context["related_add_url"]

        self.assertEqual(first=got_related_add_url, second="/app/donor/add/?_to_field=id")


class ItemAdminTestCase(TestCase):
    def setUp(self) -> None:
        self.donor = Donor.objects.create(
            donor_name="Test", contact_name="Best", email="test@example.com",
            mobile_number="+1 (234) 567-8901")

        self.donation = Donation.objects.create(donor=self.donor)
        item_device = ItemDevice.objects.create()
        self.item = Item.objects.create(donation=self.donation,
                                        device=item_device, quantity=1,
                                        working=True)

        admin_site = AdminSite()
        self.item_admin = ItemAdmin(
            model=Item, admin_site=admin_site)

        self.request_factory = RequestFactory()

        self.user = User.objects.create_superuser(
            username="tester", email="tester@example.com", password="testing")

        return super().setUp()

    def test_mark_pledged(self) -> None:
        request = self.request_factory.post(path="")
        request.user = self.user
        sessionMiddleware = SessionMiddleware()
        sessionMiddleware.process_request(request=request)
        messageMiddleware = MessageMiddleware()
        messageMiddleware.process_request(request=request)
        queryset = Item.objects.all()

        self.item_admin.mark_pledged(req=request, qs=queryset)

        want_status = ItemStatusEnum.PLEDGED.value.upper()
        self.assertEqual(first=self.item.status,
                         second=want_status)

    def test_destroy_item(self) -> None:
        request = self.request_factory.delete(path="")
        request.user = self.user
        sessionMiddleware = SessionMiddleware()
        sessionMiddleware.process_request(request=request)
        messageMiddleware = MessageMiddleware()
        messageMiddleware.process_request(request=request)
        items = Item.objects.all()

        self.item_admin.destroy_item(req=request, qs=items)

        try:
            got_item = Item.objects.get(donation=self.item.donation)
        except Item.DoesNotExist:
            got_item = None

        self.assertIsNone(obj=got_item)
