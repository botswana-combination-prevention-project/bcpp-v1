from django.conf.urls import patterns, url
from .views import replace_data, return_data, replacement_index

urlpatterns = patterns('',
    url(r'replacement_index/', replacement_index, name='replacement_index_url'),
    url(r'^return/(?P<household>[A-Z0-9\-0-9]+)/', 'return_households'),
    url(r'^replace_data/', replace_data, name='replace_data_url'),
    url(r'^return_data/', return_data, name='return_data_url')
    )
