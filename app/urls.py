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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

admin.autodiscover()

urlpatterns = [
    url(r'^', admin.site.urls),
    url(r'^add/new$', views.new_form, name='new_form'),
    url(r'^analytics$', views.get_analytics, name='get_analytics'),
    url(r'^upload/csv$', views.get_csv, name='get_csv'),
    url(r'^upload/poll_state$', views.poll_state, name='poll_state'),
    url(r'^poll_state$', views.poll_state, name='poll_state'),
    url(r'^download_pdf$', views.start_pdf_gen, name='start_pdf_gen'),
    url(r'^download/pdf/(?P<task_id>.*)',
        views.download_pdf, name='download_pdf'),
]

# API urlpatterns
urlpatterns += [
    url(r'^api/autocomplete_name/$',
        api_views.autocomplete_name,
        name='autocomplete_name'),
    url(r'^api/quantity$', data_view.aggregate_quantity, name='aggregate_quantity'),
    url(r'^api/value$', data_view.aggregate_value, name='aggregate_value'),
    url(r'^api/status$', data_view.aggregate_status, name='aggregate_status'),
    url(r'^api/donor$', login_required(DonorView.as_view(), login_url='/login')),
    url(r'^api/donation$', login_required(DonationView.as_view(), login_url='/login')),
    url(r'^api/item$', login_required(ItemView.as_view(), login_url='/login')),
]
