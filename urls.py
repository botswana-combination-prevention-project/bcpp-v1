from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^(?P<app_label>\w+)/(?P<model_name>\w+)/$', 
        'data_describer', 
        name="describer_url_name"
        ),
    url(r'', 
        'data_describer', 
        name="describer_url_name"
        ),
    )        


