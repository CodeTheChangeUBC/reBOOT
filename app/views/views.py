# -*- coding: utf-8 -*-

import csv
import simplejson as json
from celery.result import AsyncResult
from celery.states import SUCCESS
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from app.constants.field_names import FIELD_NAMES
from app.models import Donor, Donation, Item
from app.worker.parser import parser
from app.worker.exporter import exporter
from app.worker.generate_pdf import generate_pdf


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
        return _error(request, "Permission Denied. Please contact admins.")


@login_required(login_url="/login")
def get_analytics(request):
    context = _context("Analytics")
    return render(request, "app/analytics.html", context)


@login_required(login_url="/login")
def import_csv(request):
    """A view to redirect after task queuing csv parser
    """
    if "job" in request.GET:
        return _poll_state_response(request, "import_csv")
    elif request.POST:
        csv_file = request.FILES.get("uploaded_file", False)
        if csv_file and csv_file.name.endswith(".csv"):
            raw_file = csv_file.read()
            decoded_file = str(raw_file, 'utf-8', errors='ignore').splitlines()
            job = parser.delay(decoded_file)
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
def generate_receipt(request):
    """Initialize pdf generation from tasks
    Takes request from admin which contains request.queryset
    """
    if "job" in request.GET:
        return _poll_state_response(request, "generate_receipt")
    elif request.POST:
        queryset = serializers.serialize("json", request.queryset)
        job = generate_pdf.delay(queryset, len(request.queryset))
        return HttpResponseRedirect(
            reverse("generate_receipt") + "?job=" + job.id)
    else:
        return _error(request)


@login_required(login_url="/login")
def poll_state(request):
    """A view to report the progress to the user
    """
    if not (request.is_ajax() and request.POST["task_id"]):
        return _error(request)

    try:
        task_id = request.POST.get("task_id")
        task = AsyncResult(task_id)
        task_response = task.result or task.state
    except Exception:
        return _error(request)

    if task.state == SUCCESS:
        response = HttpResponse(SUCCESS)
    else:
        if isinstance(task_response, str):
            response = HttpResponse(task_response)
        else:
            response = JsonResponse(task_response)

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
        if not task.ready():
            return _error(request)
        task_response = task.result or task.state
    except Exception:
        return _error(request)

    if task.state != SUCCESS:
        return JsonResponse(task.state)

    response = _error(request)
    if task_name == "export_csv":
        response = _render_csv(task_response)
    elif _is_file(task_response):
        response = task_response

    return response


"""
Private Methods
"""


def _is_file(file):
    content_type_name = file.get("Content-Type")
    file_types = ["zip", "pdf", "csv"]
    return any(file_type in content_type_name for file_type in file_types)


def _is_zip(file):
    content_type_name = file.get("Content-Type")
    return "zip" in content_type_name


def _is_pdf(file):
    content_type_name = file.get("Content-Type")
    return "pdf" in content_type_name


def _is_csv(file):
    content_type_name = file.get("Content-Type")
    return "csv" in content_type_name


def _render_csv(response):
    """Response must be of format:
    {
        "file_name": String,
        "rows": []
    }
    """
    file = HttpResponse(content_type="application/csv")
    file["Content-Disposition"] = "attachment;filename=" + \
        response["file_name"] + ".csv"

    writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
    writer.writeheader()
    for row in response["rows"]:
        writer.writerow(row)
    return file


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


def _error(request, err_msg="Something went wrong."):
    context = _context(err_msg)
    return render(request, "app/error.html", context)
