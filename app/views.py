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
    response_data = {}
    response_data['result'] = ['Tom Lee', 'Michelle Huh', 'Omar', 'guarav']
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def get_donor_data(request):
    response_data = {}
    response_data['id_email'] = 'michelle.huh@hotmail.com'
    response_data['id_telephone_number'] = '7783203240'
    response_data['id_mobile_number'] = '7781234567'
    response_data['id_customer_ref'] = 'what is this'
    response_data['id_want_receipt'] = True
    response_data['id_address_line'] = '1234 Westbrook Mall'
    response_data['id_city'] = 'Vancouver'
    response_data['id_province'] = 'BC'
    response_data['id_postal_code'] = 'V6T 1K8'
    return HttpResponse(json.dumps(response_data), content_type="application/json")

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
