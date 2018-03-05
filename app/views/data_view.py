# -*- coding: utf-8 -*-
from app.models import Donor, Donation, Item
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views import View
import simplejson as json

# return aggregate value for given time interval
# if request.GET['interval'] is false, return value of all items
@login_required(login_url='/login')
def aggregate_value(request):
    return_value = 0
    if request.GET['interval'] is False:
        return_value = sum(Item.value for item in Item.objects.all())
    else:
        initial_date = request.GET['initial_date']
        final_date = request.GET['final_date']
        items = Item.objects.filter(
            tax_receipt_no__donate_date__gte=initial_date
        ).filter(
            tax_receipt_no__donate_date__lte=final_date
        )
        return_value = sum(Item.value for item in items)
    return return_value

# return aggregate quantity of given model for given time interval
@login_required(login_url='/login')
def aggregate_quality(request):
    model = request.GET['model']
    return_value = 0
    if request.GET['interval'] is False:
        if model is Donor:
            return_value = sum(1 for donor in Donor.objects.all(), 0)
        elif model is Donation:
            return_value = sum(1 for donation in Donation.objects.all(), 0)
        else: # model = Item
            return_value = sum(1 for item in Item.objects.all(). 0)
    else:
        initial_date = request.GET['initial_date']
        final_date = request.GET['final_date']
        data = []
        if model is Donor:
            data = Donor.objects.filter(
                created_at__gte=initial_date
            ).filter(
                created_at__lte=final_date
            )
        elif model is Donation:
            data = Donation.objects.filter(
                donate_date__gte=initial_date
            ).filter(
                donate_date__lte=final_date
            )
        else: # model = Item
            data = Item.objects.filter(
                tax_receipt_no__donate_date__gte=initial_date
            ).filter(
                tax_receipt_no__donate_date__lte=final_date
            )
        return_value = sum(1 for aData in data, 0)
    return return_value