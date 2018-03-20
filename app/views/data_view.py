# -*- coding: utf-8 -*-
from app.models import Donor, Donation, Item
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views import View
import simplejson as json

@login_required(login_url='/login')
def aggregate_value(request):
    '''if request.GET['interval'] is false, return value of all items
    otherwise, return array of values for given interval
    '''
    try:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']

        items = __getModelsGivenInterval('item', start_date, end_date)
        
        item_date_pairs = map(__generatePairs, items)
        result = {'result': item_date_pairs}

        return JsonResponse(result.serialize(), status=200)
    except BaseException:
        return HttpResponseBadRequest()


@login_required(login_url='/login')
def aggregate_quanity(request):
    '''return aggregate quantity of given model for given time interval.'''
    try:
        model = request.GET['model']
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']

        items = __getModelsGivenInterval(model, start_date, end_date)
        aggregated_quantity = sum(1 for item in items)
        result = {'result': aggregate_quanity}
        
        return JsonResponse(result.serialize(), status=200)
    except BaseException:
        return HttpResponseBadRequest

'''
Private
'''
def __getModelsGivenInterval(model, start_date, end_date):
    '''returns the given Models in given time interval.'''
    model_class = {
        'donor': Donor,
        'donation': Donation,
        'item': Item
    }

    # TODO: what to do for default case?
    if start_date != null && end_date != null:
        return model_Class.get(model, Donor).filter(created_at__range=(start_date, end_date))
    
    elif start_date != null && end_date == null:
        return model_Class.get(model, Donor).objects.filter(created_at__gte=start_date)
    
    elif start_date == null && end_date != null:
        return model_Class.get(model, Donor).objects.filter(created_at__lte=end_date)

    else # both null
        return model_Class.get(model, Donor).objects.all()

def __generatePairs(model):
    '''generate pairs of creation date and value, given element'''
    return {'date': model.created_at, 'value': model.value}