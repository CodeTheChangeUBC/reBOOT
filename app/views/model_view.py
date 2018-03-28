# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from app.models import Donor, Donation, Item
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views import View
import simplejson as json


class DonorView(View):
    '''DonorView
    - GET: Return JSON serialized Donor object
    - POST: Insert and return that Donor object
    - PUT: Update and return that Donor object
    - DELETE: Delete and return HTTP status code
    '''

    def get(self, request):
        try:
            donor = Donor.objects.get(id=request.GET['donor_id'])
            return JsonResponse(donor.serialize(), status=200)
        except BaseException:
            return HttpResponseBadRequest()

    def post(self, request):
        try:
            donor = Donor.objects.create(
                donor_name=request.POST['donor_name'],
                email=request.POST['email'],
                want_receipt=request.POST['want_receipt'],
                telephone_number=request.POST['telephone_number'],
                mobile_number=request.POST['mobile_number'],
                address_line=request.POST['address_line'],
                city=request.POST['city'],
                province=request.POST['province'],
                postal_code=request.POST['postal_code'],
                customer_ref=request.POST['customer_ref'],
                verified=request.POST['verified']
            )
            return JsonResponse(donor.serialize(), status=201)
        except BaseException:
            return HttpResponseBadRequest()

    def put(self, request):
        try:
            donor = Donor.objects.get(id=request.PUT['donor_id'])
            donor.donor_name = request.PUT['donor_name'],
            donor.email = request.PUT['email'],
            donor.want_receipt = request.PUT['want_receipt'],
            donor.telephone_number = request.PUT['telephone_number'],
            donor.mobile_number = request.PUT['mobile_number'],
            donor.address_line = request.PUT['address_line'],
            donor.city = request.PUT['city'],
            donor.province = request.PUT['province'],
            donor.postal_code = request.PUT['postal_code'],
            donor.customer_ref = request.PUT['customer_ref'],
            donor.verified = request.PUT['verified']
            donor.save()
            return JsonResponse(donor.serialize(), status=200)
        except BaseException:
            return HttpResponseBadRequest()

    def delete(self, request):
        try:
            donor = Donor.objects.get(id=request.GET['donor_id'])
            donor.delete()
            return HttpResponse(None, status=200)
        except BaseException:
            return HttpResponseBadRequest()


class DonationView(View):
    '''DonationView
    - GET: Return JSON serialized Donation objects based on donor id
    - POST: Insert and return that Donation object
    - PUT: Update and return that Donation object
    - DELETE: Delete and return HTTP status code
    '''

    def get(self, request):
        try:
            donation_list = Donation.objects.filter(
                donor_id=request.GET['donor_id'])
            response_data = [donation.serialize()
                             for donation in donation_list]
            return JsonResponse(response_data, status=200)
        except BaseException:
            return HttpResponseBadRequest()

    def post(self, request):
        try:
            donation = Donation.objects.create(
                donor_id=request.POST['donor_id'],
                tax_receipt_no=request.POST['tax_receipt_no'],
                donate_date=request.POST['donate_date'],
                verified=request.POST['verified'],
                pick_up=request.POST['pick_up']
            )
            return JsonResponse(donation.serialize(), status=200)
        except BaseException:
            return HttpResponseBadRequest()

    def put(self, request):
        try:
            donation = Donation.objects.get(
                tax_receipt_no=request.PUT['tax_receipt_no'])
            donation.donate_date = request.PUT['donate_date']
            donation.verified = request.PUT['verified']
            donation.pick_up = request.PUT['pick_up']
            donation.save()
            return JsonResponse(donor.serialize(), status=200)
        except BaseException:
            return HttpResponseBadRequest()

    def delete(self, request):
        try:
            donation = Donation.objects.get(
                tax_receipt_no=request.DELETE['tax_receipt_no'])
            donation.delete()
            return HttpResponse(None, status=200)
        except BaseException:
            return HttpResponseBadRequest()


class ItemView(View):
    '''ItemView
    - GET: Return JSON serialized Item objects based on donation id
    - POST: Insert and return Item object
    - PUT: Update and return Item object
    - DELETE: Delete and return HTTP status code
    '''

    def get(self, request):
        try:
            item_list = Item.objects.filter(
                tax_receipt_no=request.GET['tax_receipt_no'])
            response_data = [item.serialize() for item in item_list]
            return JsonResponse(response_data, status=200)
        except BaseException:
            return HttpResponseBadRequest()

    def post(self, request):
        try:
            item = Item.objects.create(
                tax_receipt_no=request.POST['tax_receipt_no'],
                description=request.POST['description'],
                particulars=request.POST['particulars'],
                manufacturer=request.POST['manufacturer'],
                model=request.POST['model'],
                quantity=request.POST['quality'],
                working=request.POST['working'],
                condition=request.POST['condition'],
                quality=request.POST['quality'],
                batch=request.POST['batch'],
                value=request.POST['value'],
                verified=request.POST['verified']
            )
            return JsonResponse(item.serialize(), status=200)
        except BaseException:
            return HttpResponseBadRequest()

    def put(self, request):
        try:
            item = Item.objects.get(id=request.PUT['item_id'])
            item.tax_receipt_no = request.PUT['tax_receipt_no']
            item.description = request.PUT['description']
            item.particulars = request.PUT['particulars']
            item.manufacturer = request.PUT['manufacturer']
            item.model = request.PUT['model']
            item.quantity = request.PUT['quality']
            item.working = request.PUT['working']
            item.condition = request.PUT['condition']
            item.quality = request.PUT['quality']
            item.batch = request.PUT['batch']
            item.value = request.PUT['value']
            item.verified = request.PUT['verified']
            item.save()
            return JsonResponse(item.serialize(), status=200)
        except BaseException:
            return HttpResponseBadRequest()

    def delete(self, request):
        try:
            item = Item.objects.get(id=request.DELETE['item_id'])
            item.delete()
            return HttpResponse(None, status=200)
        except BaseException:
            return HttpResponseBadRequest()
