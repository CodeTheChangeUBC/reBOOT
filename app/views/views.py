# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from celery.result import AsyncResult
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from app.worker.parser import parser
from app.worker.generate_pdf import generate_pdf
from app.models import Donor, Donation, Item
import csv
import simplejson as json


@login_required(login_url='/login')
def new_form(request):
    return render(request, 'app/form.html')


@login_required(login_url='/login')
def get_analytics(request):
    return render(request, 'app/analytics.html')


@login_required(login_url='/login')
def get_csv(request):
    ''' A view to redirect after task queuing csv parser
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
        if (csv_file and csv_file.name.endswith('.csv')):
            job = parser.delay(csv_file)
            return HttpResponseRedirect(reverse('get_csv') + '?job=' + job.id)
        else:
            return render(request, 'app/error.html')
    else:
        return HttpResponseRedirect('/')


'''
A view to report the progress to the user
'''


@login_required(login_url='/login')
@csrf_exempt
def poll_state(request):
    if request.is_ajax() and request.POST['task_id']:
        task_id = request.POST['task_id']
        task = AsyncResult(task_id)
        response = task.result or task.state

    if isinstance(response, dict):
        return JsonResponse(response)
    elif isinstance(response, str):
        return HttpResponse(response)
    elif __is_zip(response) or __is_pdf(response):
        # Same output as task.result in other cases
        return HttpResponse("SUCCESS")
    else:
        return response


@login_required(login_url='/login')
def start_pdf_gen(request):
    ''' Initialize pdf generation from tasks
    Takes request from admin which contains request.queryset
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
        job = generate_pdf.delay(request.queryset)
        return HttpResponseRedirect(
            reverse('start_pdf_gen') + '?job=' + job.id)
    else:
        return render(request, 'app/error.html')


def download_pdf(request, task_id):
    ''' Downloads PDF after task is complete
    '''
    task_id = 0
    try:
        task_id = request.build_absolute_uri().split("task_id=", 1)[1]
    except BaseException:
        return HttpResponseRedirect('/')

    work = AsyncResult(task_id)

    try:
        if not work.ready():
            raise FileNotFoundError()
        result = work.get(timeout=1)
        if __is_zip(result):
            return HttpResponse(result, content_type='application/zip')
        else:
            return result
    except:
        return render(request, 'app/error.html')


'''
Private Methods
'''


def __is_zip(file):
    content_type_name = file.get('Content-Type')
    return "zip" in content_type_name


def __is_pdf(file):
    content_type_name = file.get('Content-Type')
    return "pdf" in content_type_name
