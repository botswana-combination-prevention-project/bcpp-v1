from django.conf.urls import patterns, url

from edc.device.sync.exceptions import ProducerError
from edc.device.sync.utils import load_producer_db_settings

from .views import load_producer_databases


try:
    load_producer_db_settings()
except ProducerError:
    pass

urlpatterns = patterns('apps.bcpp_dispatch.views',
    url(r'^play_transactions/', 'play_transactions', name='bccp_dispatch_play_url'),
    url(r'^sync/(?P<selected_producer>[a-z0-9\-\_\.]+)/', 'bcpp_sync', name='bccp_sync_producer_url'),
    url(r'^sync/', 'bcpp_sync', name='bccp_sync_url'),
    url(r'^load_producer_databases/$', load_producer_databases, name='load_producer_databases_url'),
    url(r'^', 'bcpp_dispatch_view', name='bccp_dispatch_url'),
    )
