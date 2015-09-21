from django.conf.urls import patterns, url

from edc.device.sync.exceptions import ProducerError
from edc.device.sync.utils import load_producer_db_settings

from .views import load_producer_databases, bcpp_sync, bcpp_dispatch_view, play_transactions, export_outgoing_to_usb


try:
    load_producer_db_settings()
except ProducerError:
    pass

urlpatterns = patterns('',
    url(r'^play_transactions/', play_transactions, name='bcpp_dispatch_play_url'),
    url(r'^sync/export_outgoing_to_usb/', export_outgoing_to_usb, name='bcpp_sync_export_outgoing_url'),
    url(r'^sync/(?P<selected_producer>[a-z0-9\-\_\.]+)/', bcpp_sync, name='bcpp_sync_url'),
    url(r'^sync/', bcpp_sync, name='bcpp_sync_url'),
    url(r'^sync/', bcpp_sync, name='sync_index_url'),
    url(r'^load_producer_databases/$', load_producer_databases, name='load_producer_databases_url'),
    url(r'^', bcpp_dispatch_view, name='bcpp_dispatch_url'),
)
