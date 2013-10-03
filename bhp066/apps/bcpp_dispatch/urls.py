from django.conf.urls import patterns, url

urlpatterns = patterns('apps.bcpp_dispatch.views',
    url(r'^play_transactions/', 'play_transactions',),
    url(r'^sync/', 'bcpp_sync',),
    url(r'^', 'bcpp_dispatch',),
    )
