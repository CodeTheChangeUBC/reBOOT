# -*- coding: utf-8 -*-
from app.models import Donor, Donation, Item
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views import View
import simplejson as json
import time

@login_required(login_url='/login')
def aggregate_value(request):
    '''If request.GET['interval'] is false, return value of all items
    otherwise, return array of values for given interval
    '''
    try:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']

        items = __getModelsGivenInterval('item', start_date, end_date)

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
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']

        items = __getModelsGivenInterval(model, start_date, end_date)

        aggregated_quantity = __generatePairsWithQuantity(items)
        result = {'result': aggregated_quantity}
        
        return JsonResponse(result, status=200)
    except BaseException:
        return HttpResponseBadRequest()

'''
Private
'''
def __getModelsGivenInterval(model, start_date, end_date):
    '''Returns the given Models in given time interval.'''
    cur_model = {
        'donor': Donor,
        'donation': Donation,
        'item': Item
    }.get(model, Donor.objects.none())

    # TODO: what to do for default case?
    if start_date != None && end_date != None:
        return cur_model.filter(created_at__range=(start_date, end_date))
    
    elif start_date != None && end_date == None:
        return cur_model.objects.filter(created_at__gte=start_date)
    
    elif start_date == None && end_date != None:
        return cur_model.objects.filter(created_at__lte=end_date)

    else # both None
        return cur_model.objects.all()

def __generatePairsWithValue(objects):
    '''Generate pairs of creation date and value, given lists of objects'''
    result = {}

    for item in objects:
        formatted_date = __formatDate(item.created_at)
        exists = result.get(formatted_date)
        if exists != None:  # Already existed
            result[formatted_date] += item.value
        else:   # New date added
            result[formatted_date] = item.value

    return result

def __generatePairsWithQuantity(objects):
     '''Generate pairs of creation date and quantity, given lists of objects'''
    result = {}

    for item in objects:
        formatted_date = __formatDate(item.created_at)
        exists = result.get(formatted_date)
        if exists != None:  # Already existed
            result[formatted_date] += 1
        else:   # New date added
            result[formatted_date] = 1

    return result

def __formatDate(date):
    return time.strftime("%d-%m-%Y", date)