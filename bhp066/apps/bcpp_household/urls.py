from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('bcpp_household.views',
    url(r'^return/(?P<household>[A-Z0-9\-0-9]+)/', 'return_households'),
    url(r'^add_household_index/(?P<plot>[0-9\-0-9]+)/', add_household_index, name='add_household_index_url'),
    url(r'^add_household/(?P<plot>[0-9\-0-9]+)/', add_household, name='add_household_url')
    )