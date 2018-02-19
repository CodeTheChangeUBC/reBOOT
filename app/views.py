# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from celery.result import AsyncResult
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.views import View
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from .forms import DocumentForm
from .tasks import parser
from .models import Donor, Donation, Item
import csv
import json

import sys

@login_required(login_url='/login/?next=/')
def autocomplete_name(request):
    # request.GET['key']
    # return list of names ordered by asc
    # request.GET = request.GET.copy()
    # request.GET['model'] = 'donor'
    # request.GET['key']
    # request.GET['type'] = 'name'
    # return autocomplete(request)
    response_data = {}
    mylist = ['Tom Lee', 'Michelle Huh', 'Omar', 'Gaurav', 'Matilda', 'Michael Smith', 'Mickey Mouse', 'Thomas', 'Michelle Lee', 'John Doe', 'Joey']
    data = request.GET['key']
    response_data['result'] = list(filter(lambda x: data.upper() in x.upper(), mylist))
    return HttpResponse(json.dumps(response_data), content_type="application/json")

#@login_required(login_url='/login/?next=/')
class DonorView(View):
    response_data = [];

    def get(self, request):
        id = request.GET['donor_id']
        try:
            donor = Donor.objects.get_object_or_404(id = id)
        except:
            return HttpResponse(json.dumps(None), content_type="application/json")
        else:
            response_data.append(donor.serialize())
            return HttpResponse(json.dumps(response_data), content_type="application/json")

    def delete(self, request):
        id = request.GET['donor_id']
        donor = Donor.objects.get_object_or_404(id = id)
        donor.delete()
        # should add alter or something that says deletion completed?
        return HttpResponse(json.dumps(none), content_type="application/json")

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

    def post(self, request):
        donor = Donor(
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
        donor.save()
        return HttpResponse(json.dumps(donor.serialize()), content_type="application/json")

@login_required(login_url='/login/?next=/')
def donation(request):
    response_data = {}
    if request.GET:
        name = request.GET['donor_name'].upper()
        if name not in list(map(lambda x: x.upper(),
                                ['Tom Lee', 'Michelle Huh', 'Omar', 'Gaurav', 'Matilda', 'Michael Smith',
                                 'Mickey Mouse', 'Thomas', 'Michelle Lee', 'John Doe', 'Joey'])):
            return HttpResponse(json.dumps(None), content_type="application/json")

        response_data = {}
        response_data['donation_records'] = [{
            'tax_receipt_no': '2017-0223',
            'donate_date': 'Dec. 19, 2016',
            'pick_up': 'D/O @ M4W 3X8',
            'verified': False
        }, {
            'tax_receipt_no': '2017-0222',
            'donate_date': 'Dec. 15, 2016',
            'pick_up': 'D/O @ M4W 3X8',
            'verified': True
        }]
    elif request.POST:
        response_data = [{
            'tax_receipt_no': '2017-0223',
            'donate_date': request.POST['donate_date'],
            'pick_up': request.POST['pick_up'],
            'verified': 'verified' in request.POST
        }, {
            'tax_receipt_no': '2017-0223',
            'donate_date': '2017-02-26',
            'pick_up': 'D/O @ M4W 3X8',
            'verified': False
        }, {
            'tax_receipt_no': '2017-0222',
            'donate_date': '2017-12-30',
            'pick_up': 'D/O @ M4W 3X8',
            'verified': True
        }]
    elif request.DELETE:
        list(filter(lambda x: request.DELETE['tax_receipt_no'] not in x, response_data))


    return HttpResponse(json.dumps(response_data), content_type="application/json")

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


# Create your views here.
@login_required(login_url='/login/?next=/')
def new_form(request):
    # if request.GET:
    #     # do something
    # elif request.POST:
    #     # do something
    return render(request, 'app/form.html')

@login_required(login_url='/login/?next=/')
def get_analytics(request):
    return render(request, 'app/analytics.html')

@login_required(login_url='/login/?next=/')
def get_csv(request):
    '''
    A view to redirect after task queuing csv parser
    '''
    if 'job' in request.GET:
        job_id = request.GET['job']
        job = AsyncResult(job_id)
        data = job.result or job.state
        context = {
            'data': data,
            'task_id': job_id,
        }
        return render(request, "app/CSVworked.html", context)
    elif request.POST:
        csv_file = request.FILES.get('my_file', False)
        if(csv_file and csv_file.name.endswith('.csv')):
            job = parser.delay(csv_file)
            return HttpResponseRedirect(reverse('get_csv') + '?job=' + job.id)
        else:
            return render(request, 'app/CSVfailed.html')
    else:
        return HttpResponseRedirect('/')

@login_required(login_url='/login/?next=/')
def poll_state(request):
    '''
    A view to report the progress to the user
    '''
    
    data = 'Fail'
    if request.is_ajax():
        if 'task_id' in request.POST.keys() and request.POST['task_id']:
            task_id = request.POST['task_id']
            task = AsyncResult(task_id)
            data = task.result or task.state
        else:
            data = 'No task_id in the request'
    else:
        data = 'This is not an AJAX request'

    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

@login_required(login_url='/login/?next=/')
def autocomplete(request):
    '''
    An API endpoint that returns 5 related JSON objects filtered
    '''
    if request.is_ajax() and request.GET:
        model_type = request.GET['model']
        request_type = request.GET['type']
        param = request.GET['key']
        model_objects = {
            'donor': Donor.objects.filter(donor_name__icontains=param),
            # 'donation': Donation.objects.filter(donor_id=param),
            # 'item': Item.objects.filter(tax_receipt_no=param),
        }.get(model_type, [])
        json_array = [model.serialize() for model in list(model_objects)]
        for obj in json_array:
            obj.pop('_state') 

        if request_type is 'name':
            json_array = [obj.donor_name for obj in json_array]


        json_data = json.dumps(json_array)
        return HttpResponse(json_data, content_type='application/json')
    else:
        return HttpResponseBadRequest()
