from __future__ import unicode_literals
from app.models import Donor
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import simplejson as json

@login_required(login_url='/login')
def autocomplete_name(request):
    search_key = request.GET['key']    
    search_result = Donor.objects.filter(donor_name__icontains=search_key)
    search_result = [donor.serialize() for donor in search_result]
    response_data = [donor["donor_name"] for donor in search_result]
    print json.dumps(response_data)
    return HttpResponse(json.dumps(response_data), content_type="application/json")
