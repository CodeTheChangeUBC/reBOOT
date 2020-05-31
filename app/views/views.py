# -*- coding: utf-8 -*-
import logging
from celery.exceptions import TimeoutError
from celery.result import AsyncResult
from celery.states import PENDING, SUCCESS, FAILURE
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods, require_POST, require_GET

from app.constants.str import PERMISSION_DENIED
from app.worker.app_celery import PROGRESS, ATTEMPT_LIMIT
from app.worker.tasks.importers import historical_data_importer
from app.worker.tasks.exporter import exporter
from app.worker.tasks.create_receipt import create_receipt


logger = logging.getLogger(__name__)


@require_GET
@login_required(login_url="/login")
def new_form(request):
    """Donation Form (Deprecated)"""
    user = request.user
    if (user.has_perm('app.view_donor') and
        user.has_perm('app.view_donation') and
            user.has_perm('app.view_item')):
        context = _context("Donation Form")
        return render(request, "app/form.html", context)
    else:
        return _error(request, PERMISSION_DENIED)


@require_GET
@login_required(login_url="/login")
def get_analytics(request):
    return render(request, "app/analytics.html", _context("Analytics"))


@require_http_methods(["GET", "POST"])
@login_required(login_url="/login")
def import_csv(request):
    """A view to redirect after task queuing csv importer
    """
    if not request.user.has_perm('app.can_import_historical'):
        return _error(request, PERMISSION_DENIED)

    res = HttpResponseRedirect("/")

    if request.method == "GET":
        if "job" in request.GET:
            res = _poll_state_response(request, "import_csv")
    elif request.method == "POST":
        csv_file = request.FILES.get("uploaded_file", None)
        if csv_file and csv_file.name.endswith(".csv"):
            raw_file = csv_file.read()
            decoded_file = str(raw_file, 'utf-8-sig',
                               errors='ignore').splitlines()
            job = historical_data_importer.s(decoded_file).delay()
            res = HttpResponseRedirect(f"{reverse('import_csv')}?job={job.id}")
        else:
            res = _error(request)
    return res


@require_http_methods(["GET", "POST"])
@login_required(login_url="/login")
def export_csv(request):
    """Queue CSV exporter then redirect to poll state"""
    if not request.user.has_perm('app.can_export_data'):
        return _error(request, PERMISSION_DENIED)

    res = HttpResponseRedirect("/")

    if request.method == "GET":
        if "job" in request.GET:
            return _poll_state_response(request, "export_csv")
    elif request.method == "POST":
        export_name = request.POST.get("export_name", "export")
        job = exporter.s(export_name).delay()
        res = HttpResponseRedirect(f"{reverse('export_csv')}?job={job.id}")
    return res


@require_http_methods(["GET", "POST"])
@login_required(login_url="/login")
def download_receipt(request):
    """Initialize pdf generation from tasks
    Takes request from admin which contains request.queryset
    """
    if not request.user.has_perm('app.generate_tax_receipt'):
        return _error(request, PERMISSION_DENIED)

    res = _error(request)

    if request.method == "GET":
        if "job" in request.GET:
            res = _poll_state_response(request, "download_receipt")
    elif request.method == "POST":
        queryset = serializers.serialize("json", request.queryset)
        job = create_receipt.s(queryset, len(request.queryset)).delay()
        res = HttpResponseRedirect(
            f"{reverse('download_receipt')}?job={job.id}")
    return res


@require_POST
@login_required(login_url="/login")
def poll_state(request):
    """A view to report the progress to the user"""
    task_id = request.POST.get("task_id", None)
    if task_id is None:
        return _error(request)

    task = AsyncResult(task_id)
    res = JsonResponse(_poll_state(PENDING, 0, 200))
    if task.state == FAILURE or task.failed():
        res = JsonResponse(_poll_state(FAILURE, 0, 400))
    elif task.state == PROGRESS:
        res = JsonResponse(task.result) if isinstance(
            task.result, dict) else HttpResponse(task.result)
    elif task.state == SUCCESS or task.successful() or task.ready():
        res = HttpResponse(SUCCESS)
    return res


@require_GET
@login_required(login_url="/login")
def download_file(request):
    """Downloads file after task is complete
    """
    try:
        task_id = request.GET.get("task_id")
        task_name = request.GET.get("task_name", "task")
        attempts = 0
        # CloudAMQP free tier is unstable and must be circuit breakered
        while(attempts < ATTEMPT_LIMIT):
            try:
                attempts += 1
                task = AsyncResult(task_id)
                result = task.get(timeout=0.5*attempts)
                print(f"{task} {task_name} success #{attempts}: {result}")
                break
            except TimeoutError:
                print(f"{task} {task_name} failed #{attempts}")
                if (attempts >= ATTEMPT_LIMIT):
                    return _error(request, "Download exceeded max attempts")
        return result
    except Exception as e:
        return _error(request, "Something went wrong.", e)


def error(request):
    """Error page"""
    return _error(request)


"""
Private Methods
"""


def _poll_state_response(request, task_name):
    context = _context("Poll State", {
        "task_id": request.GET["job"],
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
    # logger.exception(err_msg)
    return render(request, "app/error.html", _context(err_msg))


def _poll_state(state, percent, status):
    return {
        "state": state,
        "process_percent": percent,
        "status": status,
    }
