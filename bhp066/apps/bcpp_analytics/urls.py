from django.conf.urls import patterns, url
from .views import index, accrual
from .views import operational_report_view


urlpatterns = patterns('',
                       url(r'^reports/$', index),
                       url(r'^report/community_accrual/$', accrual, name="accrual"),
                       url(r'^report/operational/', operational_report_view, name="operational"),
                       )
