# -*- coding: utf-8 -*-
from app.models import Donor, Donation, Item
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.db.models import Sum, Count, F, FloatField
from django.views.decorators.http import require_GET


@require_GET
@login_required(login_url='/login')
def aggregate_value(request):
    """If request.GET['interval'] is false, return JSON of value of all items
    otherwise, return JSON of array of values for given interval
    """
    try:
        model = request.GET.get('model', 'item')
        start_date = request.GET.get('startDate', None)
        end_date = request.GET.get('endDate', None)

        items = __getQuerysetGivenInterval(model, start_date, end_date)

        agg_values = list(items.values('documented_at')
                               .annotate(
                                   total_value=Sum(
                                       F('value')*F('quantity'),
                                       output_field=FloatField())))
        result = {'result': __castDecimalToFloat(agg_values)}

        return JsonResponse(result, status=200)
    except BaseException as e:
        print(e.args)
        return HttpResponseBadRequest()


@require_GET
@login_required(login_url='/login')
def aggregate_quantity(request):
    """Return JSON of aggregate quantity of given model for given time interval."""
    try:
        model = request.GET['model']
        start_date = request.GET.get('startDate', None)
        end_date = request.GET.get('endDate', None)

        items = __getQuerysetGivenInterval(model, start_date, end_date)

        # Count all models as 1 except for items which has quantity field
        count_method = Count('pk') if model != 'item' else Sum('quantity')

        agg_qty = list(items.values('documented_at')
                            .annotate(total_quantity=count_method))
        result = {'result': agg_qty}

        return JsonResponse(result, status=200)
    except BaseException as e:
        print(e.args)
        return HttpResponseBadRequest()


@require_GET
@login_required(login_url='/login')
def aggregate_status(request):
    """Return aggregate status of item for given time interval."""
    try:
        model = 'item'
        start_date = request.GET.get('startDate', None)
        end_date = request.GET.get('endDate', None)

        items = __getQuerysetGivenInterval(model, start_date, end_date)

        agg_status = list(items.values('status')
                               .annotate(count=Count('status')))

        result = {'result': agg_status}

        return JsonResponse(result, status=200)
    except BaseException as e:
        print(e.args)
        return HttpResponseBadRequest()


@require_GET
@login_required(login_url='/login')
def aggregate_location(request):
    """Return a JSON of province and item_quantity"""
    try:
        start_date = request.GET.get('startDate', None)
        end_date = request.GET.get('endDate', None)

        items = __getQuerysetGivenInterval('item', start_date, end_date)

        items_grouped_by_location = list(
            items.annotate(location=F('donation__donor__city'))
            .values('location')
            .annotate(count=Count('location'))
        )
        result = {'result': items_grouped_by_location}

        return JsonResponse(result, status=200)
    except BaseException as e:
        print(e.args)
        return HttpResponseBadRequest()


"""
Private
"""


def __getQuerysetGivenInterval(model, start_date, end_date):
    """Returns the given Models in given time interval."""
    cur_model = {
        'donor': Donor,
        'donation': Donation,
        'item': Item
    }.get(model, Donor.objects.none())

    # might need following lines when changing back to created_at:
    # date_format = "%Y-%m-%d"
    # if start_date is not None:
    #     timezone_unaware_start_date = datetime.strptime(start_date, date_format)
    #     timezone_aware_start_date = pytz.utc.localize(timezone_unaware_start_date)
    #
    # if end_date is not None:
    #     timezone_unaware_end_date = datetime.strptime(end_date, date_format)
    #     timezone_aware_end_date = pytz.utc.localize(timezone_unaware_end_date).date()

    if start_date is not None and end_date is not None:
        return cur_model.objects.filter(documented_at__range=(start_date, end_date))
    elif start_date is not None and end_date is None:
        return cur_model.objects.filter(documented_at__gte=start_date)
    elif start_date is None and end_date is not None:
        return cur_model.objects.filter(documented_at__lte=end_date)
    else:
        return cur_model.objects.all()


def __castDecimalToFloat(lists):
    for pair in lists:
        pair['total_value'] = float(
            "{:.2f}".format(float(pair['total_value'])))
    return lists
