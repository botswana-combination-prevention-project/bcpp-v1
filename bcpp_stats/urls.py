from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('bhp_model_describer.views',
    url(r'^model_describer/', 'model_describer', name="describer_url_name" ),
    )
