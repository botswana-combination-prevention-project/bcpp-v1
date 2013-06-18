from django.conf.urls.defaults import patterns, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('bhp_birt_reports.views',
    url(r'^generate_report/', 'generate_report'),
    url(r'^report_parameters/', 'report_parameters'),
    #url(r'^return_selectively/(?P<producer>[a-z0-9\-\_\.]+)/', 'return_selectively'),
    #url(r'^', 'return_items',),
    )
