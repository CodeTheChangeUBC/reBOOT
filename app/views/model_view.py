# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from app.models import Donor, Donation, Item
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
import simplejson as json

'''
DonorView
 - GET: Return JSON serialized Donor object
 - POST: Insert and return that Donor object
 - PUT: Update and returnn that Donor object
 - DELETE: Delete and return HTTP status code
'''
class DonorView(View):
    def get(self, request):
        try:
            donor = Donor.objects.get(id = request.GET['donor_id'])
            return HttpResponse(json.dumps(donor.serialize()), content_type="application/json", status=200)            
        except:
            return HttpResponseBadRequest()

    def post(self, request):
        try:
            donor = Donor.objects.create(
                donor_name = request.POST['donor_name'],
                email = request.POST['email'],
                want_receipt = request.POST['want_receipt'],
                telephone_number = request.POST['telephone_number'],
                mobile_number = request.POST['mobile_number'],
                address_line = request.POST['address_line'],
                city = request.POST['city'],
                province = request.POST['province'],
                postal_code = request.POST['postal_code'],
                customer_ref = request.POST['customer_ref'],
                verified = request.POST['verified']
            )
            return HttpResponse(json.dumps(donor.serialize()), content_type="application/json", status=201)
        except:
            return HttpResponseBadRequest() 

    def put(self, request):
        try:
            donor = Donor.objects.get(id = request.GET['donor_id'])
            donor.donor_name = request.GET['donor_name'],
            donor.email = request.GET['email'],
            donor.want_receipt = request.GET['want_receipt'],
            donor.telephone_number = request.GET['telephone_number'],
            donor.mobile_number = request.GET['mobile_number'],
            donor.address_line = request.GET['address_line'],
            donor.city = request.GET['city'],
            donor.province = request.GET['province'],
            donor.postal_code = request.GET['postal_code'],
            donor.customer_ref = request.GET['customer_ref'],
            donor.verified = request.GET['verified']
            donor.save()
            return HttpResponse(json.dumps(donor.serialize()), content_type="application/json", status=200)
        except:
            return HttpResponseBadRequest()

    def delete(self, request):
        try:
            donor = Donor.objects.get(id = request.GET['donor_id'])
            donor.delete()
            return HttpResponse(json.dumps(None), content_type="application/json", status=200)
        except:
            return HttpResponse(json.dumps(None), content_type="application/json", status=400)

'''
DonationView
 - GET: Return JSON serialized Donation objects based on donor id
 - POST: Insert and return that Donation object
 - PUT: Update and return that Donation object
 - DELETE: Delete and return HTTP status code
'''
class DonationView(View):
    def get(self, request):
        donation_list = Donation.objects.filter(donor_id=request.GET['donor_id'])
        response_data = [donation.serialize() for donation in donation_list]
        return HttpResponse(json.dumps(response_data), content_type='application/json')

    def post(self, request):
        donation = Donation.objects.create(
            donor_id = request.POST['donor_id'],
            tax_receipt_no = request.POST['tax_receipt_no'],
            donate_date = request.POST['donate_date'],
            verified = request.POST['verified'],
            pick_up = request.POST['pick_up']
        )
        return HttpResponse(json.dumps(donation.serialize()), content_type='application/json')

    def put(self, request):
        try:
            donation = Donation.objects.get(tax_receipt_no = request.PUT['tax_receipt_no'])
            donation.donate_date = request.PUT['donate_date']
            donation.verified = request.PUT['verified']
            donation.pick_up = request.PUT['pick_up']
            donation.save()
            return HttpResponse(json.dumps(donor.serialize()), content_type='application/json', status=200)
        except:
            return HttpResponse(json.dumps(None), content_type='application/json', status=400)

    def delete(self, request):
        try:
            donation = Donation.objects.get(tax_receipt_no = request.DELETE['tax_receipt_no'])
            donation.delete()
            return HttpResponse(json.dumps(None), content_type="application/json", status=200)
        except:
            return HttpResponseBadRequest()

'''
ItemView
 - GET: Return JSON serialized Item objects based on donation id
 - POST: Insert and return Item object
 - PUT: Update and return Item object
 - DELETE: Delete and return HTTP status code
'''
class ItemView(View):
    def get(self, request):
        try:
            item = Item.objects.get(id = request.GET['item_id'])
            return HttpResponse(json.dumps(item.serialize()), content_type="application/json", status=200)
        except:
            return HttpResponseBadRequest()

    def post(self, request):
        try:
            item = Item.objects.create(
                tax_receipt_no = request.POST['tax_receipt_no'],
                description = request.POST['description'],
                particulars = request.POST['particulars'],
                manufacturer = request.POST['manufacturer'],
                model = request.POST['model'],
                quantity = request.POST['quality'],
                working = request.POST['working'],
                condition = request.POST['condition'],
                quality = request.POST['quality'],
                batch = request.POST['batch'],
                value = request.POST['value'],
                verified = request.POST['verified']
            )
            return HttpResponse(json.dumps(item.serialize()), content_type="application/json", status=200)
        except:
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
            return HttpResponse(json.dumps(item.serialize()), content_type="application/json", status=200)
        except:
            return HttpResponseBadRequest()
    def delete(self, request):
        try:
            item = Item.objects.get(id=request.DELETE['item_id'])
            item.delete()
            return HttpResponse(json.dumps(None), content_type="application/json", status=200)
        except:
            return HttpResponseBadRequest()
