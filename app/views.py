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

        csv_file = request.FILES['my_file']
        if(csv_file.name.endswith('.csv')):
            parser(csv_file)

            return HttpResponse(csv_file)
        else:
            return HttpResponse("<h1> Invalid format </h1>")
    else:
        return HttpResponse("<h1> DId not work</h1> ")
