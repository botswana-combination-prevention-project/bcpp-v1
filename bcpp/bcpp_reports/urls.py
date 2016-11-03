from django.conf.urls import patterns, url
from .views import operational_report_view

urlpatterns = patterns('',
                       url(r'^operational/', operational_report_view,),
                       )
