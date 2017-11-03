# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .forms import DocumentForm
from django.shortcuts import render
from .csvparser import parser

# Create your views here.
def get_csv(request):
    if "POST" == request.method:
        csv_file = request.FILES.get('my_file', False)
        if(csv_file and csv_file.name.endswith('.csv')):
            # parser(csv_file)
            return render(request, 'app/CSVworked.html')
        else:
            return render(request, 'app/CSVfailed.html')
    else:
        return HttpResponseRedirect('/')