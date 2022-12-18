from app.models import Donor, Donation, Item, ItemDevice
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Q
import simplejson as json


@login_required(login_url='/login')
@require_GET
def autocomplete_name(request):
    try:
        search_key = request.GET['key']
        search_result = Donor.objects.filter(
            donor_name__icontains=search_key).order_by('id')
        search_result = [donor.camel_serialize() for donor in search_result]
        return HttpResponse(json.dumps(search_result),
                            content_type="application/json")
    except Exception as e:
        return HttpResponse(e, content_type="application/json")


@login_required(login_url='/login')
@require_GET
def donor_info_auto_complete(request):
    try:
        search_key = request.GET['filter']
        donor_tups = list(Donor.objects.filter(
            donor_name__icontains=search_key).values_list(
            "donor_name", "id").order_by('donor_name'))
        donor_infos = [
            f"{donor_tup[0]} | {donor_tup[1]}" for donor_tup in donor_tups]
        return JsonResponse({'donorInfos': donor_infos})
    except Exception as e:
        return JsonResponse(e, safe=False)


@login_required(login_url='/login')
@require_GET
def device_info_auto_complete(request):
    try:
        search_key = request.GET['filter']
        devices = ItemDevice.objects.filter(
            Q(make__icontains=search_key) | Q(model__icontains=search_key))
        device_infos = [
            f"{d} | {d.dtype} | {d.id}" for d in devices]
        device_infos.sort(key=lambda d: d.lower())
        return JsonResponse({'deviceInfos': device_infos})
    except Exception as e:
        return JsonResponse(e, safe=False)


@login_required(login_url='/login')
@require_GET
def related_donations(request):
    try:
        donation_list = Donation.objects.filter(
            donor__id=request.GET['donorId']
        )
        response = [donation.camel_serialize() for donation in donation_list]
        return JsonResponse(response, safe=False, status=200)
    except Exception as e:
        return JsonResponse(e, safe=False)


@login_required(login_url='/login')
@require_GET
def related_items(request):
    try:
        items_list = Item.objects.filter(
            donation__tax_receipt_no=request.GET['taxReceiptNo']
        )
        response = [item.underscore_serialize() for item in items_list]
        return JsonResponse(response, safe=False, status=200)
    except Exception as e:
        return JsonResponse(e, safe=False)
