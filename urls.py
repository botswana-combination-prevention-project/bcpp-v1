from django.conf.urls.defaults import patterns, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^return/(?P<producer>[a-z0-9\-\_\.]+)/', 'return_items'),
    url(r'^return/(?P<identifier>\w+)/', 'return_households', name='return_household'),
    #url(r'^return_selectively/(?P<producer>[a-z0-9\-\_\.]+)/', 'return_selectively'),
    #url(r'^', 'return_items',),
    )
