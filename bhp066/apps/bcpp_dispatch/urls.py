from django.conf.urls import patterns, url

urlpatterns = patterns('apps.bcpp_dispatch.views',
    url(r'^play_transactions/', 'play_transactions', name='bccp_dispatch_play_url'),
    url(r'^sync/(?P<selected_producer>[a-z0-9\-\_\.]+)/', 'bcpp_sync', name='bccp_sync_producer_url'),
    url(r'^sync/', 'bcpp_sync', name='bccp_sync_url'),
    url(r'^', 'bcpp_dispatch_view', name='bccp_dispatch_url'),
    )
