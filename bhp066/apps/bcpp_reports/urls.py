from django.conf.urls import patterns, url

from .views import index, accrual

urlpatterns =  patterns('',
    url(r'^reports/$', index),
    url(r'^reports/community_accrual/$', accrual, name="accrual"),
)
