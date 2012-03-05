#from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver        
from base_transaction import BaseTransaction
from bhp_sync.classes import DeserializeFromTransaction


class IncomingTransaction(BaseTransaction):
    
    
    class Meta:
        app_label = 'bhp_sync'   
        ordering = ['timestamp']
        
        
@receiver(post_save,)
def deserialize_on_post_save(sender, instance, **kwargs):
    if isinstance(instance, IncomingTransaction):
        DeserializeFromTransaction.deserialize(sender, instance, **kwargs)