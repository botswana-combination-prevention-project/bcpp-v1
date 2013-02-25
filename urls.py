from django.conf.urls.defaults import patterns, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('bhp_dispatch.views',
    url(r'^return/(?P<producer>[a-z0-9\-\_\.]+)/', 'return_items'),
    #url(r'^return_dashboard/(?P<household>[A-Z0-9\-0-9]+)/', 'return_items_from_dashboard'),
    #url(r'^', 'return_items',),
    )