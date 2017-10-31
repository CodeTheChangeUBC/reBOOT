# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

from django.shortcuts import render

# Create your views here.
def get_csv(request):
    if request.method == 'POST' and request.FILES['my_file']:
        myfile = request.FILES['my_files']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)


        return HttpResponse("<h1> It worked </h1>")

    else:
        return HttpResponse("<h1> It failed </h1> ")
