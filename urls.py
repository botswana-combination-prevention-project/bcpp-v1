from django.conf.urls.defaults import patterns, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('bcpp_household.views',
    url(r'^return/(?P<household>[A-Z0-9\-0-9]+)/', 'return_households'),
    )
