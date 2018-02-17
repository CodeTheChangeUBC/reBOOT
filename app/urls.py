"""reboot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^', admin.site.urls),
    url(r'^add/get_donor_data', views.donor, name='donor'),
    url(r'^add/donation', views.donation, name='donation'),
    url(r'^add/item', views.item, name='item'),
    url(r'^add/new$', views.new_form, name='new_form'),
    url(r'^add/autocomplete_name$', views.autocomplete_name, name='autocomplete_name'),
    url(r'^analytics$', views.get_analytics, name='get_analytics'),
    url(r'^upload/csv$', views.get_csv, name='get_csv'),
    url(r'^upload/poll_state$', views.poll_state, name='poll_state'),
    url(r'^api/autocomplete$', views.autocomplete, name='autocomplete'),
]
