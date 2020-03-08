# -*- coding: utf-8 -*-
import csv
import logging
import simplejson as json
from celery.result import AsyncResult
from celery.states import PENDING, SUCCESS
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from app.constants.str import PERMISSION_DENIED
from app.models import Donor, Donation, Item
from app.worker.importers import historical_data_importer
from app.worker.exporter import exporter
from app.worker.create_receipt import create_receipt


logger = logging.getLogger('app.views')


@login_required(login_url="/login")
def new_form(request):
    """Donation Form
    """
    user = request.user
    if (user.has_perm('app.view_donor') and
        user.has_perm('app.view_donation') and
            user.has_perm('app.view_item')):
        context = _context("Donation Form")
        return render(request, "app/form.html", context)
    else:
        return _error(request, PERMISSION_DENIED)


@login_required(login_url="/login")
def get_analytics(request):
    context = _context("Analytics")
    return render(request, "app/analytics.html", context)


@login_required(login_url="/login")
def import_csv(request):
    """A view to redirect after task queuing csv importer
    """
    if not request.user.has_perm('app.can_import_historical'):
        return _error(request, PERMISSION_DENIED)

    if "job" in request.GET:
        return _poll_state_response(request, "import_csv")
    elif request.POST:
        csv_file = request.FILES.get("uploaded_file", False)
        if csv_file and csv_file.name.endswith(".csv"):
            raw_file = csv_file.read()
            decoded_file = str(raw_file, 'utf-8', errors='ignore').splitlines()
            job = historical_data_importer.delay(decoded_file)
            return HttpResponseRedirect(
                reverse("import_csv") + "?job=" + job.id)
        else:
            return _error(request)
    else:
        return HttpResponseRedirect("/")


@login_required(login_url="/login")
def export_csv(request):
    """A view to redirect after task queuing csv exporter
    """
    if not request.user.has_perm('app.can_export_data'):
        return _error(request, PERMISSION_DENIED)

    if "job" in request.GET:
        return _poll_state_response(request, "export_csv")
    elif request.POST:
        export_name = request.POST.get("export_name", "export")
        job = exporter.delay(export_name)
        return HttpResponseRedirect(
            reverse("export_csv") + "?job=" + job.id)
    else:
        return HttpResponseRedirect("/")


@login_required(login_url="/login")
def download_receipt(request):
    """Initialize pdf generation from tasks
    Takes request from admin which contains request.queryset
    """
    if not request.user.has_perm('app.generate_tax_receipt'):
        return _error(request, PERMISSION_DENIED)

    if "job" in request.GET:
        return _poll_state_response(request, "download_receipt")
    elif request.POST:
        queryset = serializers.serialize("json", request.queryset)
        job = create_receipt.delay(queryset, len(request.queryset))
        return HttpResponseRedirect(
            reverse("download_receipt") + "?job=" + job.id)
    else:
        return _error(request)


@login_required(login_url="/login")
def poll_state(request):
    """A view to report the progress to the user
    """
    response = HttpResponse(status=404)
    if request.POST and request.POST["task_id"]:
        task_id = request.POST["task_id"]
        task = AsyncResult(task_id)
        task_response = task.result or task.state

    if task != None and task.state == SUCCESS:
        response = HttpResponse(SUCCESS)
    elif isinstance(task_response, str):
        response = HttpResponse(task_response)
    elif isinstance(task_response, dict):
        response = JsonResponse(task_response)
    else:
        response = task_response

    # If task complete, return success
    return response


@login_required(login_url="/login")
def download_file(request, task_id=0):
    """Downloads file after task is complete
    """
    try:
        task_id = request.GET.get("task_id")
        task_name = request.GET.get("task_name", None)
        task = AsyncResult(task_id)
        task_response = task.result or task.state
        result = task.get()
        return result
    except Exception as e:
        return _error(request, "download failed", e)


def error(request):
    """Error page
    """
    return _error(request)


"""
Private Methods
"""


def _poll_state_response(request, task_name):
    job_id = request.GET["job"]
    job = AsyncResult(job_id)
    data = job.result or job.state
    context = _context("Poll State", {
        "data": data,
        "task_id": job_id,
        "task_name": task_name
    })
    return render(request, "app/PollState.html", context)


def _context(title, override={}):
    context = {
        "title": title,
        "has_permission": True,
    }
    context.update(override)
    return context


def _error(request, err_msg="Something went wrong.", e=None):
    logger.error("%s error:" % (request.get_full_path(), err_msg), e)
    return render(request, "app/error.html", _context(err_msg))
