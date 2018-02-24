# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from app.models import Donor, Donation, Item
from django.views import View

'''
DonorView
 - GET: return JSON serialized Donor object
 - POST: Insert into the database and return that object
 - PUT: 
 - DELETE: 
'''
class DonorView(View):
    response_data = [];

    def get(self, request):
        try:
            id = request.GET['donor_id']
            donor = Donor.objects.get_object_or_404(id = id)
        except:
            return HttpResponse(json.dumps(None), content_type="application/json", status=404)
        else:
            return HttpResponse(json.dumps(donor.serialize()), content_type="application/json", status=200)

    def post(self, request):
        try:
            donor = Donor.objects.create(
                donor_name = request.GET['donor_name'],
                email = request.GET['email'],
                want_receipt = request.GET['want_receipt'],
                telephone_number = request.GET['telephone_number'],
                mobile_number = request.GET['mobile_number'],
                address_line = request.GET['address_line'],
                city = request.GET['city'],
                province = request.GET['province'],
                postal_code = request.GET['postal_code'],
                customer_ref = request.GET['customer_ref'],
                verified = request.GET['verified']
            )
        except:
            return 
        return HttpResponse(json.dumps(donor.serialize()), content_type="application/json")

    def put(self, request):
        id = request.GET['donor_id']
        try:
            donor = Donor.objects.get_object_or_404(id = id)
        except:
            raise Http404("Donor does not exist")
        else:
            donor.update(
                donor_name = request.GET['donor_name'],
                email = request.GET['email'],
                want_receipt = request.GET['want_receipt'],
                telephone_number = request.GET['telephone_number'],
                mobile_number = request.GET['mobile_number'],
                address_line = request.GET['address_line'],
                city = request.GET['city'],
                province = request.GET['province'],
                postal_code = request.GET['postal_code'],
                customer_ref = request.GET['customer_ref'],
                verified = request.GET['verified'])
            return HttpResponse(json.dumps(donor.serialize()), content_type="application/json")

    def delete(self, request):
        id = request.GET['donor_id']
        donor = Donor.objects.get_object_or_404(id = id)
        donor.delete()
        # should add alter or something that says deletion completed?
        return HttpResponse(json.dumps(none), content_type="application/json")

'''
DonationView
 - GET: return JSON serialized Donation object
 - POST: Insert into the database and return that object
 - PUT: 
 - DELETE: 
'''
class DonationView(View):
    response_data = []

    def get(self, request):
        donation_list = Donation.objects.select_related().filter(donor_id=request.GET['donor_id'])
        for donation in donation_list:
            response_data.append(donation.serialize())
        return HttpResponse(json.dumps(response_data), content_type='application/json')

    def post(self, request):
        donor_id = request.POST['donor_id']
        tax_receipt_no = request.POST['tax_receipt_no']
        donate_date = request.POST['donate_date']
        verified = request.POST['verified']
        pick_up = request.POST['pick_up']
        donation = Donation.objects.create(
            donor_id = donor_id,
            tax_receipt_no = tax_receipt_no,
            donate_date = donate_date,
            verified = verified,
            pick_up = pick_up)
        response_data.append(donation.serialize())
        return HttpResponse(json.dumps(response_data), content_type='application/json')

    def delete(self, request):
        try:
            donation = Donation.objects.get(request.DELETE['donor_id'])
        except (Donation.DoesNotExist):
            return HttpResponse(json.dumps({"Fail: donation does not exist."}), content_type='application/json')
        else:
            donation.delete()
            return HttpResponse(json.dumps({"Success"}), content_type='application/json')
    
    def put(self, request):
        try:
            donor_id = request.PUT['donor_id']
            tax_receipt_no = request.PUT['tax_receipt_no']
            donate_date = request.PUT['donate_date']
            verified = request.PUT['verified']
            pick_up = request.PUT['pick_up']
        except KeyError:
            return HttpResponse(json.dumps("Fail: invalid scheme for update."), content_type='application/json')
        try:
            donation = Donation.objects.get(tax_receipt_no = tax_receipt_no)
        except (Donation.DoesNotExist):
            return HttpResponse(json.dumps("Fail: donation does not exist."))
        donation.donor_id = donor_id
        donation.donate_date = donate_date
        donation.verified = verified
        donation.pick_up = pick_up
        donation.save()
        return HttpResponseRedirect(reverse())



    # def delete(self, request):
    #     return render(...)

'''
ItemView
 - GET: return JSON serialized Item object
 - POST: Insert into the database and return that object
 - PUT: 
 - DELETE: 
'''
class ItemView(View):
    response_data = []
    def get(self, request):
        id = request.GET['item_id']
        try:
            item = Item.objects.get_object_or_404(id = id)
        except:
            return HttpResponse(json.dumps(None), content_type="application/json")
        else:
            response_data.append(item.serialize())
            # should add alter or something that says deletion completed?
            return HttpResponse(json.dumps(response_data), content_type="application/json")


    def put(self, request):
        id = request.GET['item_id']
        try:
            itemExist = Item.objects.get_object_or_404(id = id)
        except:
            raise Http404("Item does not exist")
        else:
            item = Item(
                QUALITY = 'Medium',
                tax_receipt_no = request.GET['tax_receipt_no'],
                description = request.GET['description'],
                particulars = request.GET['particulars'],
                manufacturer = request.GET['manufacturer'],
                model = request.GET['model'],
                quantity = request.GET['quality'],
                working = request.GET['working'],
                condition = request.GET['condition'],
                quality = request.GET['quality'],
                batch = request.GET['batch'],
                value = request.GET['value'],
                verified = request.GET['verified']
            )
            item.save()
            return HttpResponse(json.dumps(none), content_type="application/json")

    def post(self, request):
        item = Item(
            QUALITY = 'Medium',
            tax_receipt_no = request.GET['tax_receipt_no'],
            description = request.GET['description'],
            particulars = request.GET['particulars'],
            manufacturer = request.GET['manufacturer'],
            model = request.GET['model'],
            quantity = request.GET['quality'],
            working = request.GET['working'],
            condition = request.GET['condition'],
            quality = request.GET['quality'],
            batch = request.GET['batch'],
            value = request.GET['value'],
            verified = request.GET['verified']
        )
        item.save()
        return HttpResponse(json.dumps(none), content_type="application/json")

    def delete(self, request):
        id = request.GET['item_id']
        item = Item.objects.get(id=id)
        item.delete()
        return HttpResponse(json.dumps(none), content_type="application/json")
