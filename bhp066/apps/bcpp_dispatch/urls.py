from django.conf.urls import patterns, url

urlpatterns = patterns('apps.bcpp_dispatch.views',
    url(r'^', 'bcpp_dispatch',),
    )
