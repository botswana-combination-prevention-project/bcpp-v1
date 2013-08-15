from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from api import OutgoingTransactionMiddleManResource, OutgoingTransactionServerResource, MiddleManTransactionResource

admin.autodiscover()
outgoing_transaction_middle_man_resource = OutgoingTransactionMiddleManResource()
outgoing_transaction_server_resource = OutgoingTransactionServerResource()
middle_man_transaction_resource = MiddleManTransactionResource()

urlpatterns = patterns('',
    (r'^api_otmr/', include(outgoing_transaction_middle_man_resource.urls)),
    (r'^api_otsr/', include(outgoing_transaction_server_resource.urls)),
    (r'^api_mmtr/', include(middle_man_transaction_resource.urls)),
    )

urlpatterns += patterns('bhp_sync.views',
    # fetch unsent transactions from a producer (GET)
    url(r'^consume/(?P<producer>[a-z0-9\-\_\.]+)/', 'consume_transactions',),
    url(r'^view/(?P<model_name>incomingtransaction|outgoingtransaction|middlemantransaction)/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/', 'view_transaction', name='view_transaction_url',),
    url(r'^consumed/(?P<selected_producer>[a-z0-9\-\_\.]+)/', 'index',),
    url(r'^$', 'index',),
    )
