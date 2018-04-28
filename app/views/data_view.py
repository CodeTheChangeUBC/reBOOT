# -*- coding: utf-8 -*-
from app.models import Donor, Donation, Item
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.db.models import Sum, Count, F

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

        item_date_pairs = list(items.values('created_at_formatted').annotate(total_value=Sum('value')))
        result = {'result': item_date_pairs}

        return JsonResponse(result, status=200)
    except BaseException as e:
        print e.args
        return HttpResponseBadRequest()

@login_required(login_url='/login')
def aggregate_quantity(request):
    """Return JSON of aggregate quantity of given model for given time interval."""
    try:
        model = request.GET['model']
        start_date = request.GET.get('startDate', None)
        end_date = request.GET.get('endDate', None)

        items = __getQuerysetGivenInterval(model, start_date, end_date)

        aggregated_quantity = list(items.values('created_at_formatted').annotate(total_quantity=Count('created_at')))
        result = {'result': aggregated_quantity}
        
        return JsonResponse(result, status=200)
    except BaseException as e:
        print e.args
        return HttpResponseBadRequest()

@login_required(login_url='/login')
def aggregate_location(request):
    """Return a JSON of province and item_quantity"""
    try:
        start_date = request.GET.get('startDate', None)
        end_date = request.GET.get('endDate', None)

        items = __getQuerysetGivenInterval('item', start_date, end_date)

        items_grouped_by_location = list(items.annotate(location=F('tax_receipt_no__donor_id__city')).values('location').annotate(count=Count('location')))
        result = {'result': items_grouped_by_location}

        return JsonResponse(result, status=200)
    except BaseException as e:
        print e.args
        return HttpResponseBadRequest()

'''
Private
'''
def __getQuerysetGivenInterval(model, start_date, end_date):
    '''Returns the given Models in given time interval.'''
    cur_model = {
        'donor': Donor,
        'donation': Donation,
        'item': Item
    }.get(model, Donor.objects.none())

    if start_date is not None and end_date is not None:
        return cur_model.objects.filter(created_at__range=(start_date, end_date))
    elif start_date is not None and end_date is None:
        return cur_model.objects.filter(created_at__gte=start_date)
    elif start_date is None and end_date is not None:
        return cur_model.objects.filter(created_at__lte=end_date)
    else:
        return cur_model.objects.all()

def __formatDate(date):
    return date.strftime("%Y-%m-%d")