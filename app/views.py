# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from celery.result import AsyncResult
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest

from django.contrib.auth.decorators import login_required
#
from django.views.generic import TemplateView
from django.views import View

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from .forms import DocumentForm
from .tasks import parser
from .models import Donor, Donation, Item
import csv
import simplejson as json

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

@login_required(login_url='/login/?next=/')
def donor(request):

    # request.GET['donor_name']
    # return donor_info + donation_records
    response_data = {}

    if request.GET:
        name = request.GET['donor_name'].upper()
        if name not in list(map(lambda x: x.upper(),
                                ['Tom Lee', 'Michelle Huh', 'Omar', 'Gaurav', 'Matilda', 'Michael Smith',
                                 'Mickey Mouse', 'Thomas', 'Michelle Lee', 'John Doe', 'Joey'])):
            return HttpResponse(json.dumps(None), content_type="application/json")

        response_data = {}

        response_data['name'] = request.GET['donor_name']
        response_data['email'] = name.lower().replace(' ', '.') + '@ubc.ca'
        response_data['telephone_number'] = '7783203240'
        response_data['mobile_number'] = '7781234567'
        response_data['customer_ref'] = 'what is this'
        response_data['want_receipt'] = True
        response_data['address_line'] = '1234 Westbrook Mall'
        response_data['city'] = 'Vancouver'
        response_data['province'] = 'BC'
        response_data['postal_code'] = 'V6T 1K8'
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
    # elif (request.POST):
        # respond with customer ref
    # elif (request.DELETE):
        # respond with something
    # else:

    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required(login_url='/login/?next=/')
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
            verified = verified
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
        response_data['email'] = name.lower().replace(' ', '.') + '@ubc.ca'
        response_data['telephone_number'] = '7783203240'
        response_data['mobile_number'] = '7781234567'
        response_data['customer_ref'] = 'what is this'
        response_data['want_receipt'] = True
        response_data['address_line'] = '1234 Westbrook Mall'
        response_data['city'] = 'Vancouver'
        response_data['province'] = 'BC'
        response_data['postal_code'] = 'V6T 1K8'
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

@login_required(login_url='/login/?next=/')
def item(request):
    dummy_data = {
        '2017-0222': [{
                    'item_id': 6547,
                    'manufacturer': 'Generic',
                    'model': '0',
                    'quantity': 1,
                    'batch': 'B2016-0431',
                    'verified': True
                }, {
                    'item_id': 6548,
                    'manufacturer': 'AMD',
                    'model': 'ALKE8Y-JWRWHQI',
                    'quantity': 1,
                    'batch': 'B2016-0432',
                    'verified': True
                }, {
                    'item_id': 6549,
                    'manufacturer': 'Samsung',
                    'model': 'A98-B087',
                    'quantity': 3,
                    'batch': 'B2017-0431',
                    'verified': False
                }, ],
        '2017-0223': [{
                    'item_id': 1111,
                    'manufacturer': 'Apple',
                    'model': 'SJHD87382390DSJKW8952Y9',
                    'quantity': 100,
                    'batch': 'B2018-0431',
                    'verified': True
                }]
    }
    response_data = {}

    if request.GET:
        if 'item_id' in request.GET:
            response_data = {
                'itemId': request.GET['item_id'],
                'description': 'graphic card',
                'particulars': 'none',
                'manufacturer': 'AMD',
                'model': 'ALKE8Y-JWRWHQI',
                'quantity': 1,
                'isWorking': True,
                'condition': 'Good',
                'quality': 'H',
                'isVerified': True,
                'batch': 'B2016-0432',
                'value': 10,
            }
        else:
            # return list
            response_data = dummy_data[request.GET['tax_receipt_no']]
    # elif request.PUT:
    # elif request.POST:
    # elif request.DELETE:

    return HttpResponse(json.dumps(response_data), content_type="application/json")

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
