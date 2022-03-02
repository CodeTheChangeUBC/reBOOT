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
            donor_name__icontains=search_key
        ).order_by('id')
        search_result = [donor.camel_serialize() for donor in search_result]
        return HttpResponse(json.dumps(search_result),
                            content_type="application/json")
    except:
        return HttpResponse('', content_type="application/json")


@login_required(login_url='/login')
@require_GET
def donor_names(request):
    try:
        donor_names = list(Donor.objects.values_list("donor_name", flat=True).order_by('donor_name'))
        return JsonResponse({'donorNames': donor_names},
                            content_type="application/json")
    except Exception as e:
        return JsonResponse(e, safe=False)


@login_required(login_url='/login')
@require_GET
def device_names(request):
    try:
        device_objs = []
        for device in ItemDevice.objects.all():
            if device.dtype is not None:
                deviceInfo = f"{device.dtype.device_type} \
                    ({device.make}-{device.model})"
                device_objs.append(deviceInfo)

        return JsonResponse({'deviceNames': device_objs},
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
