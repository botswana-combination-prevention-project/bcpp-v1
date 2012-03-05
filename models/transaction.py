# requires django-extensions 0.7
from base_transaction import BaseTransaction


class Transaction(BaseTransaction):
    
    class Meta:
        app_label = 'bhp_sync'   
        ordering = ['timestamp'] 
