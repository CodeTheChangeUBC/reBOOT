from __future__ import unicode_literals
from app.models import Donor

@login_required(login_url='/login')
def autocomplete_name(request):
    # request.GET['key']
    # return list of names ordered by asc
    # request.GET = request.GET.copy()
    # request.GET['model'] = 'donor'
    # request.GET['key']
    # request.GET['type'] = 'name'
    # return autocomplete(request)
    response_data = {}
    mylist = ['Tom Lee', 'Michelle Huh', 'Omar', 'Gaurav', 'Matilda', 'Michael Smith', 'Mickey Mouse', 'Thomas', 'Michelle Lee', 'John Doe', 'Joey']
    data = request.GET['key']
    response_data['result'] = list(filter(lambda x: data.upper() in x.upper(), mylist))
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url='/login')
def autocomplete(request):
    '''
    An API endpoint that returns 5 related JSON objects filtered
    '''
    if request.is_ajax() and request.GET:
        model_type = request.GET['model']
        request_type = request.GET['type']
        param = request.GET['key']
        model_objects = {
            'donor': Donor.objects.filter(donor_name__icontains=param),
            # 'donation': Donation.objects.filter(donor_id=param),
            # 'item': Item.objects.filter(tax_receipt_no=param),
        }.get(model_type, [])
        json_array = [model.serialize() for model in list(model_objects)]
        for obj in json_array:
            obj.pop('_state') 

        if request_type is 'name':
            json_array = [obj.donor_name for obj in json_array]


        json_data = json.dumps(json_array)
        return HttpResponse(json_data, content_type='application/json')
    else:
        return HttpResponseBadRequest()