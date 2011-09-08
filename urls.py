from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('lab_clinic_api.views',
    url(r'^', 
        'index', 
        name="lab_clinic_api_index_url"
        ),
    )        
