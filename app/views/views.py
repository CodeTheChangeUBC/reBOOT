# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from celery.result import AsyncResult
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.views import View
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from app.worker.parser import parser
from app.worker.generate_pdf import generate_pdf
from app.models import Donor, Donation, Item
import csv
import simplejson as json

'''
@login_required(login_url='/login')
def donor(request):

    # request.GET['donor_name']
    # return donor_info + donation_records
    response_data = {}
    mylist = ['Tom Lee', 'Michelle Huh', 'Omar', 'Gaurav', 'Matilda', 'Michael Smith', 'Mickey Mouse', 'Thomas', 'Michelle Lee', 'John Doe', 'Joey']
    data = request.GET['key']
    response_data['result'] = list(filter(lambda x: data.upper() in x.upper(), mylist))
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required(login_url='/login')
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
    elif request.method == 'POST':
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

@login_required(login_url='/login')
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
'''

# Create your views here.
@login_required(login_url='/login')
def new_form(request):
    # if request.GET:
    #     # do something
    # elif request.POST:
    #     # do something
    return render(request, 'app/form.html')

@login_required(login_url='/login')
def get_analytics(request):
    return render(request, 'app/analytics.html')

@login_required(login_url='/login')
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
        return render(request, "app/PollState.html", context)
    elif request.POST:
        csv_file = request.FILES.get('my_file', False)
        if(csv_file and csv_file.name.endswith('.csv')):
            job = parser.delay(csv_file)
            return HttpResponseRedirect(reverse('get_csv') + '?job=' + job.id)
        else:
            return render(request, 'app/error.html')
    else:
        return HttpResponseRedirect('/')

@login_required(login_url='/login')
@csrf_exempt
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

    try:
        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type='application/json')
    except:
        return HttpResponse("Not JSON") # Used to check for none JSON data returns



#initialize pdf generation from tasks, takes request from admin which contains request.queryset
@login_required(login_url='/login')
def start_pdf_gen(request):
    if 'job' in request.GET:
        job_id = request.GET['job']
        job = AsyncResult(job_id)
        data = job.result or job.state
        context = {
            'data': data,
            'task_id': job_id,
        }
        try:
            return render(request, "app/PollState.html", context)
        except:
            return HttpResponseRedirect('/')

    elif request.method == 'POST':
            job = generate_pdf.delay(request.queryset)
            return HttpResponseRedirect(reverse('start_pdf_gen') + '?job=' + job.id)
    else:
        return HttpResponseRedirect('/')

#Downloads PDF after task is complete
def download_pdf(request, task_id):

    task_id = 0
    try:
        task_id = request.build_absolute_uri().split("task_id=", 1)[1]
    except:
        return HttpResponseRedirect('/')

    work = AsyncResult(task_id)

    if work.ready():
        try:
            result = work.get(timeout=1)
            content_type_name = result.get('Content-Type')

            if "zip" in content_type_name:
                return HttpResponse(result, content_type='application/zip')
            else:
                return result
        except:
            return HttpResponseRedirect('/')

    return render(request, 'app/error.html')
