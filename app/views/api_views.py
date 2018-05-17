from __future__ import unicode_literals
from app.models import Donor
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import simplejson as json


@login_required(login_url='/login')
def autocomplete_name(request):
    try:
        search_key = request.GET['key']
        search_result = Donor.objects.filter(donor_name__icontains=search_key).order_by('id')
        search_result = [donor.camel_serialize() for donor in search_result]
        return HttpResponse(json.dumps(search_result),
                            content_type="application/json")
    except:
        return HttpResponse('', content_type="application/json")
