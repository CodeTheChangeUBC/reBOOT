# -*- coding: utf-8 -*-
import logging

from celery.exceptions import TimeoutError
from celery.result import AsyncResult
from celery.states import FAILURE, PENDING, SUCCESS
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import (
    require_GET,
    require_http_methods,
    require_POST,
)

from app.constants.str import PERMISSION_DENIED
from app.models import Item
from app.worker.app_celery import ATTEMPT_LIMIT, PROGRESS
from app.worker.tasks import receiptor
from app.worker.tasks.exporter import exporter
from app.worker.tasks.importers import (
    historical_data_importer,
    webform_data_importer,
)

logger = logging.getLogger(__name__)


@require_GET
@login_required(login_url="/login")
def get_analytics(request: HttpRequest):
    return render(request, "app/analytics.html", _context("Analytics"))


def import_view_template(request, importer, filetype, required_permission):
    """A importer view template
    """
    if not request.user.has_perm(required_permission):
        return _error(request, PERMISSION_DENIED)

    res = HttpResponseRedirect("/")

    if request.method == "GET":
        if "job" in request.GET:
            res = _poll_state_response(request, "import_csv")
    elif request.method == "POST":
        uploaded_file = request.FILES.get("uploaded_file", None)
        if uploaded_file and uploaded_file.name.endswith(filetype):
            raw_file = uploaded_file.read()
            decoded_file = str(raw_file, 'utf-8-sig',
                               errors='ignore').splitlines()
            job = importer.s(decoded_file).delay()
            res = HttpResponseRedirect(f"{reverse('import_csv')}?job={job.id}")
        else:
            res = _error(request)
    return res


@require_http_methods(["GET", "POST"])
@login_required(login_url="/login")
def import_csv(request: HttpRequest):
    """A view to redirect after task queuing csv importer
    """
    return import_view_template(
        request, historical_data_importer, ".csv", "app.can_import_historical")


@require_http_methods(["GET", "POST"])
@login_required(login_url="/login")
def import_webform(request: HttpRequest):
    """A view to redirect after task queuing webform importer
    """
    return import_view_template(
        request, webform_data_importer, ".csv", "app.can_import_website")


@require_http_methods(["GET", "POST"])
@login_required(login_url="/login")
def export_csv(request: HttpRequest):
    """Queue CSV exporter then redirect to poll state"""
    if not request.user.has_perm('app.can_export_data'):
        return _error(request, PERMISSION_DENIED)

    res = HttpResponseRedirect("/")

    if request.method == "GET":
        if "job" in request.GET:
            return _poll_state_response(request, "export_csv")
    elif request.method == "POST":
        export_name = request.POST.get("export_name", "export")
        queryset = request.queryset if hasattr(request, 'queryset') \
            else Item.objects.all()
        rows = serializers.serialize("json", queryset)
        job = exporter.s(export_name, rows, len(queryset)).delay()
        res = HttpResponseRedirect(f"{reverse('export_csv')}?job={job.id}")
    return res


@require_http_methods(["GET", "POST"])
@login_required(login_url="/login")
def download_receipt(request: HttpRequest):
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
        job = receiptor.s(queryset, len(request.queryset)).delay()
        res = HttpResponseRedirect(
            f"{reverse('download_receipt')}?job={job.id}")
    return res


@require_POST
@login_required(login_url="/login")
def poll_state(request: HttpRequest):
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
def download_file(request: HttpRequest):
    """Downloads file after task is complete
    """
    try:
        task_id = request.GET.get("task_id")
        task_name = request.GET.get("task_name", "task")
        attempts = 0
        # CloudAMQP free tier is unstable and must be circuit breakered
        while (attempts < ATTEMPT_LIMIT):
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


def _poll_state_response(request: HttpRequest, task_name):
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


def _error(request: HttpRequest, err_msg="Something went wrong.", e=None):
    # logger.exception(e)
    return render(request, "app/error.html", _context(err_msg))


def _poll_state(state, percent, status):
    return {
        "state": state,
        "process_percent": percent,
        "status": status,
    }
