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
from .tasks import generate_pdf
from django.views.decorators.csrf import csrf_exempt
from celery.result import AsyncResult
from django.core.urlresolvers import reverse
import csv
import json
import zipfile
from django.views.decorators.csrf import csrf_exempt


globalData = 0
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
        return render(request, "app/PollState.html", context)
    elif (request.method == 'POST'):
        csv_file = request.FILES.get('my_file', False)
        if(csv_file and csv_file.name.endswith('.csv')):
            job = parser.delay(csv_file)
            return HttpResponseRedirect(reverse('get_csv') + '?job=' + job.id)
        else:
            return render(request, 'app/CSVfailed.html')
    else:
        return HttpResponseRedirect('/')

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
        globalData = data
        return HttpResponse(globalData)


#initailizes pdf generation from tasks
def start_pdf_gen(request):
    if 'job' in request.GET:
        job_id = request.GET['job']
        job = AsyncResult(job_id)
        data = job.result or job.state
        context = {
            'data': data,
            'task_id': job_id,
        }
        print(job.state)
        # if(data == "PENDING"):
        #     return HttpResponse(job, content_type='application/zip')
        return render(request, "app/PollState.html", context)
    elif (request.method == 'POST'):
            job = generate_pdf.delay(request.queryset);
            return HttpResponseRedirect(reverse('start_pdf_gen') + '?job=' + job.id)
    else:
        return HttpResponseRedirect('/')

#Downloads PDF after task is complete

def download_pdf(request, task_id):
    #data = request.POST['my_file']
    #print(len(data[0]))
    #print(len(data))
    task_id = request.build_absolute_uri().split("task_id=", 1)[1]                      #builds task id from URL
    print(request.build_absolute_uri())                                                 #debugging purposes
    print request.build_absolute_uri().split("task_id=", 1)[1]                          #debugging purposes
    work = AsyncResult(task_id)                                                         #get the work from ID
    if (work.ready()):                                                                  #check if it is complete
        try:
            print("is ready")
            result = work.get(timeout=1)                                                #get result of work
            try:
                filetype = str(result)                                                  #check filetype
                if(zipfile.is_zipfile(filetype)):
                    return HttpResponse(result, content_type='application/zip')         #return zip
                else:
                    return result                                                       #return pdf
            except:
                return HttpResponse(result, content_type ='application/zip')            #complete failure, return zip
        except:
            print("not ready")
            return HttpResponse("<h1> Failed </h1>")
    else:
        return HttpResponse("<h1> Failed </h1>")

