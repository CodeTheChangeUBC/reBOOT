# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Form
from .models import Raw

# Register your models here.

admin.site.register(Form)
admin.site.register(Raw)
