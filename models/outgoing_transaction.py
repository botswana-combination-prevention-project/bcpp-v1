#from django.db import models
from base_transaction import BaseTransaction


class OutgoingTransaction(BaseTransaction):
    
    
    class Meta:
        app_label = 'bhp_sync'   
        ordering = ['timestamp']