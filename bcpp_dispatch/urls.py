from django.conf.urls import patterns, url

urlpatterns = patterns('bcpp_dispatch.views',
    url(r'^', 'bcpp_dispatch',),
    )
