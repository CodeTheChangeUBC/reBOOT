"""
reboot URL Configuration

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
from app.views import views, api_views, data_view
from app.views.model_view import DonorView, ItemView, DonationView
from django.contrib.auth.decorators import login_required

admin.autodiscover()

urlpatterns = [
    url(r'^', admin.site.urls),
    url(r'^add/new$', views.new_form, name='new_form'),
    url(r'^analytics$', views.get_analytics, name='get_analytics'),
    url(r'^upload/csv$', views.import_csv, name='import_csv'),
    url(r'^upload/poll_state$', views.poll_state, name='poll_state'),
    url(r'^download/csv$', views.export_csv, name='export_csv'),
    url(r'^download/pdf$', views.generate_receipt, name='generate_receipt'),
    url(r'^download/(?P<task_id>.*)$',
        views.download_file, name='download_file'),
]

# API urlpatterns
urlpatterns += [
    url(r'^api/autocomplete_name$', api_views.autocomplete_name),
    url(r'^api/related_donations$', api_views.related_donations),
    url(r'^api/related_items$', api_views.related_items),
    url(r'^api/quantity$', data_view.aggregate_quantity, name='aggregate_quantity'),
    url(r'^api/value$', data_view.aggregate_value, name='aggregate_value'),
    url(r'^api/status$', data_view.aggregate_status, name='aggregate_status'),
    url(r'^api/location$', data_view.aggregate_location, name='aggregate_location'),
    url(r'^api/donor$', login_required(DonorView.as_view(), login_url='/login')),
    url(r'^api/donation$', login_required(DonationView.as_view(), login_url='/login')),
    url(r'^api/item$', login_required(ItemView.as_view(), login_url='/login')),
]
