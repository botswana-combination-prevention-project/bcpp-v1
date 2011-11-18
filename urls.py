from django.conf.urls.defaults import *
from django.contrib import admin
from api import TransactionResource

admin.autodiscover()
transaction_resource = TransactionResource()

urlpatterns = patterns('',
    (r'^api/', include(transaction_resource.urls)),
    )

urlpatterns += patterns('bhp_sync.views',    
    url(r'^send/', 'send_new_transactions',),
    #url(r'^', 'tx_to_response', name="tx"),
    )    
    



