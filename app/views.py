# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from celery.result import AsyncResult
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .forms import DocumentForm
from .tasks import parser
import csv
import json



def autocomplete_name(request):
    # request.GET['key']
    # return list of names ordered by asc
    response_data = {}
    response_data['result'] = ['Tom Lee', 'Michelle Huh', 'Omar', 'guarav']
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def get_donor_data(request):
    # request.GET['donor_name']
    # return donor_info + donation_records
    response_data = {}
    response_data['email'] = 'michelle.huh@hotmail.com'
    response_data['telephone_number'] = '7783203240'
    response_data['mobile_number'] = '7781234567'
    response_data['customer_ref'] = 'what is this'
    response_data['want_receipt'] = True
    response_data['address_line'] = '1234 Westbrook Mall'
    response_data['city'] = 'Vancouver'
    response_data['province'] = 'BC'
    response_data['postal_code'] = 'V6T 1K8'
    response_data['donation_records'] = [{
        'tax_receipt_no':'2017-0223',
        'donate_date':'Dec. 19, 2016',
        'pick_up': 'D/O @ M4W 3X8',
        'verified': False
    }, {
        'tax_receipt_no':'2017-0222',
        'donate_date':'Dec. 15, 2016',
        'pick_up': 'D/O @ M4W 3X8',
        'verified': True
    }]

    return HttpResponse(json.dumps(response_data), content_type="application/json")

def save_donation_data(request):
    # [tax_receipt_no, tax_receipt_no, donate_date, pick_up]
    # return updated list
    response_data = [{
        'tax_receipt_no':'2017-0224',
        'donate_date':'May. 15, 2017',
        'pick_up': 'D/O @ M4W 3X8',
        'verified': False
    }, {
        'tax_receipt_no':'2017-0223',
        'donate_date':'Dec. 19, 2016',
        'pick_up': 'D/O @ M4W 3X8',
        'verified': False
    }, {
        'tax_receipt_no':'2017-0222',
        'donate_date':'Dec. 15, 2016',
        'pick_up': 'D/O @ M4W 3X8',
        'verified': True
    }]

    return HttpResponse(json.dumps(response_data), content_type="application/json")

# not used
def get_donation_data(request):
    # request.GET['tax_receipt_no']
    response_data = {
        'tax_receipt_no' : '2017-0224',
        'donate_date' : 'May. 15, 2017',
        'pick_up' : 'D/O @ M4W 3X8',
        'verified' : False
    }

    return HttpResponse(json.dumps(response_data), content_type="application/json")

def get_items(request):
    # request.GET['tax_receipt_no']
    # return item list

    response_data = []
    if (request.GET['tax_receipt_no'] == '2017-0222'):
        response_data = [{
            'item_id': 6547,
            'manufacturer': 'Generic',
            'model': '0',
            'quantity': 1,
            'batch':'B2016-0431',
            'verified':True
        }, {
            'item_id': 6548,
            'manufacturer': 'AMD',
            'model': 'ALKE8Y-JWRWHQI',
            'quantity': 1,
            'batch':'B2016-0432',
            'verified':True
        }, {
            'item_id': 6549,
            'manufacturer': 'Samsung',
            'model': 'A98-B087',
            'quantity': 3,
            'batch':'B2017-0431',
            'verified':False
        }, ]
    elif (request.GET['tax_receipt_no'] == '2017-0223'):
        response_data = [{
            'item_id': 1111,
            'manufacturer': 'Apple',
            'model': 'SJHD87382390DSJKW8952Y9',
            'quantity': 100,
            'batch': 'B2018-0431',
            'verified': True
        }]
    else:
        respond_data = []

    return HttpResponse(json.dumps(response_data), content_type="application/json")


# def get_item_data(request):

# Create your views here.
def new_form(request):
    # if request.GET:
    #     # do something
    # elif request.POST:
    #     # do something
    return render(request, 'app/form.html')


def get_analytics(request):
    return render(request, 'app/analytics.html')

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
