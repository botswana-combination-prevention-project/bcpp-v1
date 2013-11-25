from django.conf.urls import patterns, url
from .views import operational_report

urlpatterns = patterns('',
    url(r'^operational/', operational_report,),
    )
