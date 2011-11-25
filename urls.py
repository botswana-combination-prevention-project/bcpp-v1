from django.conf.urls.defaults import *
from django.contrib import admin
from api import TransactionResource

admin.autodiscover()
transaction_resource = TransactionResource()

urlpatterns = patterns('',
    (r'^api/', include(transaction_resource.urls)),
    )

urlpatterns += patterns('bhp_sync.views',    

    # fetch unsent transactions from a producer (GET)
    url(r'^get/(?P<producer>[a-z0-9\-\_]+)/', 'get_new_transactions',),
    # send all unsent transactions to a consumer (POST)
    url(r'^post/(?P<consumer>[a-z0-9\-\_]+)/$', 'post_new_transactions',),    
    #url(r'^', 'tx_to_response', name="tx"),
    url(r'^', 'index',),
    )    
    



