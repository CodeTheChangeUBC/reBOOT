# -*- coding: utf-8 -*-
import csv
import logging
import simplejson as json
from celery.exceptions import TimeoutError
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
from app.worker.app_celery import PROGRESS, ATTEMPT_LIMIT
from app.worker.importers import historical_data_importer
from app.worker.exporter import exporter
from app.worker.create_receipt import create_receipt


logger = logging.getLogger(__name__)


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
            job = historical_data_importer.s(decoded_file).delay()
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
        job = exporter.s(export_name).delay()
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
        job = create_receipt.s(queryset, len(request.queryset)).delay()
        return HttpResponseRedirect(
            reverse("download_receipt") + "?job=" + job.id)
    else:
        return _error(request)


@login_required(login_url="/login")
def poll_state(request):
    """A view to report the progress to the user
    """
    if not request.POST or not request.POST["task_id"]:
        return _error(request, "Invalid request. Please check the request.")
    task_id = request.POST["task_id"]
    # task_name = request.POST.get("task_name", "task")
    task = AsyncResult(task_id)

    # attempts = 0
    # while (attempts < ATTEMPT_LIMIT):
    #     try:
    #         attempts += 1
    #         task = AsyncResult(task_id)
    #         if task.state != PENDING:
    #             break
    #         task.get(timeout=0.1*attempts)
    #         print(task_name, "success", attempts,
    #               "task:", task, "state", task.state)
    #     except TimeoutError:
    #         print(task_name, "fail", attempts,
    #               "task:", task, "state", task.state)
    if task.state == SUCCESS or task.successful() or task.ready():
        response = HttpResponse(SUCCESS)
    elif task.state == PROGRESS:
        if isinstance(task.result, dict):
            response = JsonResponse(task.result)
        else:  # isinstance(task.result, str)
            response = HttpResponse(task.result)
    else:  # task.state == PENDING
        response = JsonResponse({'state': PENDING, 'process_percent': 0})

    return response


@login_required(login_url="/login")
def download_file(request):
    """Downloads file after task is complete
    """
    try:
        task_id = request.GET.get("task_id")
        task_name = request.GET.get("task_name", "task")
        attempts = 0
        # prod task get is unstable and must be circuit breakered
        while(attempts < ATTEMPT_LIMIT):
            try:
                attempts += 1
                task = AsyncResult(task_id)
                result = task.get(timeout=0.5*attempts)
                print(task_name, "success", attempts,
                      "task:", task, "result:", result)
                break
            except TimeoutError:
                print(task_name, "failed", attempts, "task:", task)
                if (attempts >= ATTEMPT_LIMIT):
                    return _error(request, "download failed")
        # task.forget()
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
    context = _context("Poll State", {
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
    logger.exception(err_msg)
    return render(request, "app/error.html", _context(err_msg))
