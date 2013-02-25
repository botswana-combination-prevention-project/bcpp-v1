from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from api import OutgoingTransactionResource

admin.autodiscover()
outgoing_transaction_resource = OutgoingTransactionResource()

urlpatterns = patterns('',
    (r'^api/', include(outgoing_transaction_resource.urls)),
    )

urlpatterns += patterns('bhp_sync.views',
    # fetch unsent transactions from a producer (GET)
    url(r'^consume/(?P<producer>[a-z0-9\-\_\.]+)/', 'consume_transactions',),
    url(r'^view/(?P<model_name>incomingtransaction)/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/', 'view_transaction', name='view_transaction_url',),
    url(r'^$', 'index',),
    )
