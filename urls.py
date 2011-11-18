from django.conf.urls.defaults import *
from django.contrib import admin
from api import TransactionResource

admin.autodiscover()
transaction_resource = TransactionResource()

urlpatterns = patterns('',
    (r'^api/', include(transaction_resource.urls)),
    url(r'^', 'tx_to_response', name="tx"),
    )    
    



