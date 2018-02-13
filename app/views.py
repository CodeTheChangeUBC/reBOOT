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


# Create your views here.
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
    elif (request.method == 'POST'):
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

def autocomplete(request):
    '''
    An API endpoint that returns 5 related JSON objects filtered
    '''
    json_data = None
    if request.is_ajax() and request.GET:
        model_type = request.GET['model']
        param = request.GET['query']
        model_objects = {
            'donor': Donor.objects.filter(donor_name__contains=param),
            'donation': Donation.objects.filter(donor_id=param),
            'item': Item.objects.filter(tax_receipt_no=param),
        }.get(model_type, [])
        json_array = []
         [model.serialize() for model in list(model_objects)] # Wait for serialize() to be implemented
        for obj in list(model_objects):
            json_dict = model.serialize()
            

        json_data = json.dumps(json_array)
    else:
        json_data = json.dumps('Error: Something went wrong.')
    return HttpResponse(json_data, content_type='application/json')
