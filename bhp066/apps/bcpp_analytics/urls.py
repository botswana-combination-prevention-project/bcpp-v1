from datetime import date
from django.conf.urls import patterns, url
from .views import index, accrual, accrual_pdf
from .views import operational_report_view


urlpatterns = patterns('',
                       url(r'^reports/$', index),
                       url(r'^report/community_accrual/$', accrual, name="accrual"),
                       url(r'^report/community_accrual/pdf/(?P<com1>\w+)/(?P<com2>\w+)/(?P<start>[a-zA-Z0-9_., ]+)/(?P<to>[a-zA-Z0-9_., ]+)/$',
                           accrual_pdf, name="accrual_pdf"),
                       url(r'^report/operational/$', operational_report_view, name="operational"),
                       )
