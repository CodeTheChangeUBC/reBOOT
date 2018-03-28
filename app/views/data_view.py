# -*- coding: utf-8 -*-
from app.models import Donor, Donation, Item
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
import time

@login_required(login_url='/login')
def aggregate_value(request):
    '''If request.GET['interval'] is false, return value of all items
    otherwise, return array of values for given interval
    '''
    try:
        model = request.GET.get('model', 'item')
        start_date = request.GET.get('startDate', None)
        end_date = request.GET.get('endDate', None)

        items = __getQuerysetGivenInterval(model, start_date, end_date)

        item_date_pairs = __generatePairsWithValue(items)
        result = {'result': item_date_pairs}

        return JsonResponse(result, status=200)
    except BaseException:
        return HttpResponseBadRequest()


@login_required(login_url='/login')
def aggregate_quantity(request):
    '''Return aggregate quantity of given model for given time interval.'''
    try:
        model = request.GET['model']
        start_date = request.GET.get('startDate', None)
        end_date = request.GET.get('endDate', None)
        items = __getQuerysetGivenInterval(model, start_date, end_date)
        aggregated_quantity = __generatePairsWithQuantity(items)
        result = {'result': aggregated_quantity}
        
        return JsonResponse(result, status=200)
    except BaseException:
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

def __generatePairsWithValue(objects):
    '''Generate pairs of creation date and value, given lists of objects'''
    result = {}

    for item in objects:
        formatted_date = __formatDate(item.created_at)
        if formatted_date in result:
            result[formatted_date] += item.value
        else:
            result[formatted_date] = item.value

    return result

def __generatePairsWithQuantity(objects):
    '''Generate pairs of creation date and quantity, given lists of objects'''
    result = {}

    for item in objects:
        formatted_date = __formatDate(item.created_at)
        if formatted_date in result:
            result[formatted_date] += 1
        else:
            result[formatted_date] = 1

    return result

def __formatDate(date):
    return date.strftime("%Y-%m-%d")