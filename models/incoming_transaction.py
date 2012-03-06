#from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver        
from base_transaction import BaseTransaction
from bhp_sync.classes import DeserializeFromTransaction


class IncomingTransaction(BaseTransaction):

    """ transactions received from a remote producer and to be consumed locally"""

    class Meta:
        app_label = 'bhp_sync'   
        ordering = ['timestamp'] 
  
        
@receiver(post_save, sender=IncomingTransaction,  dispatch_uid="deserialize_on_post_save")
def deserialize_on_post_save(sender, instance, **kwargs):
    if isinstance(instance, IncomingTransaction):
        if not instance.is_consumed and not instance.is_error:
            deserialize_from_transaction = DeserializeFromTransaction()
            deserialize_from_transaction.deserialize(sender, instance, **kwargs)
        
