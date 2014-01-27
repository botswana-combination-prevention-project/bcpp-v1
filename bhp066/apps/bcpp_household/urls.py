from django.conf.urls import patterns, url
from .views import replacement_data, return_data

urlpatterns = patterns('',
    url(r'^return/(?P<household>[A-Z0-9\-0-9]+)/', 'return_households'),
    url(r'^replacement_data/', replacement_data, name='replacement_data_url'),
    url(r'^return_data/', return_data, name='return_data_url')
    )
