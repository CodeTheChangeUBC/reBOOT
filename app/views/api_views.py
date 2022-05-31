from app.models import Donor, Donation, Item, ItemDevice
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
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
    except:
        return HttpResponse('', content_type="application/json")


@login_required(login_url='/login')
@require_GET
def donor_info_auto_complete(request):
    try:
        donor_tups = list(Donor.objects.values_list(
            "donor_name", "id").order_by('donor_name'))
        donor_infos = []
        for donor_tup in donor_tups:
            donor_info = f"{donor_tup[0]} | {donor_tup[1]}"
            donor_infos.append(donor_info)

        return JsonResponse({'donorInfos': donor_infos},
                            content_type="application/json")
    except Exception as e:
        return JsonResponse(e, safe=False)


@login_required(login_url='/login')
@require_GET
def device_info_auto_complete(request):
    try:
        device_infos = []
        for d in ItemDevice.objects.all():
            if d.dtype is not None:
                device_infos.append(
                    f"{d.dtype.device_type} | {d.make}-{d.model} | {d.id}"
            )
        device_infos.sort(key=lambda d: d.lower())
        return JsonResponse({'deviceInfos': device_infos},
                            content_type="application/json")
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
    except:
        return JsonResponse([], safe=False)


@login_required(login_url='/login')
@require_GET
def related_items(request):
    try:
        items_list = Item.objects.filter(
            donation__tax_receipt_no=request.GET['taxReceiptNo']
        )
        response = [item.underscore_serialize() for item in items_list]
        return JsonResponse(response, safe=False, status=200)
    except:
        return JsonResponse([], safe=False)
