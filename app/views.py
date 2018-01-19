# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .forms import DocumentForm
from django.shortcuts import render
#from .utils import parser
from .tasks import parser
from .tasks import generate_pdf
from django.views.decorators.csrf import csrf_exempt
from celery.result import AsyncResult
from django.core.urlresolvers import reverse
import json
import csv
import zipfile


# Create your views here.
def get_csv(request):
    if 'job' in request.GET:
        job_id = request.GET['job']
        job = AsyncResult(job_id)
        data = job.result or job.state
        context = {
            'data': data,
            'task_id': job_id,
        }
        return render(request, "app/CSVworked.html", context)
    elif ("POST" == request.method):
        csv_file = request.FILES.get('my_file', False)
        if(csv_file and csv_file.name.endswith('.csv')):
            job = parser.delay(csv_file)
            return HttpResponseRedirect(reverse('get_csv') + '?job=' + job.id)
        else:
            return render(request, 'app/CSVfailed.html')
    else:
        return HttpResponseRedirect('/')


def poll_state(request):
    """ A view to report the progress to the user """
    data = 'Fail'
    if request.is_ajax():
        if 'task_id' in request.POST.keys() and request.POST['task_id']:
            task_id = request.POST['task_id']
            task = AsyncResult(task_id)
            data = task.result or task.state
        else:
            data = 'No task_id in the request'
    else:
        data = 'This is not an ajax request'

    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')


#Generates PDF responses by calling django workers.
#2018-01-18 Still causing timeout issues.
def gen_pdf(request, queryset):
    result = generate_pdf.delay(queryset)
    result_output = result.wait(timeout=None, interval=0.5)
    try:
        filetype = str(result_output)
        if(zipfile.is_zipfile(filetype)):
            return HttpResponse(result_output, content_type='application/zip')
        else:
            return HttpResponse(result_output, content_type='application/pdf')
    except:
        return HttpResponse(result_output, content_type='application/zip')