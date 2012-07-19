import socket
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver        
from base_transaction import BaseTransaction
from bhp_sync.classes import DeserializeFromTransaction


class IncomingTransaction(BaseTransaction):
    
    """ Transactions received from a remote producer and to be consumed locally. """
    
    is_self = models.BooleanField(
        default = False,
        db_index = True,
        )
        
    def save(self, *args, **kwargs):
        
        """ An incoming transaction produced by self may exist, but is not wanted, if received by fanout from a consumer of
        transactions of self (this producer). that is (hostname_modified==hostname)."""
        #TODO: for IncomingTransaction perhaps just cancel save instead??
        if self.hostname_modified == socket.gethostname():
            #self.is_consumed = True
            self.is_self = True
            
        super(IncomingTransaction, self).save(*args, **kwargs)    
    
    class Meta:
        app_label = 'bhp_sync'   
        ordering = ['timestamp'] 
  
        
@receiver(post_save, sender=IncomingTransaction,  dispatch_uid="deserialize_on_post_save")
def deserialize_on_post_save(sender, instance, **kwargs):
    
    """ Callback to deserialize an incoming transaction.
    
    as long as the transaction is not consumed or in error"""
    
    if isinstance(instance, IncomingTransaction):
        if not instance.is_consumed and not instance.is_error: # and not instance.is_self:
            deserialize_from_transaction = DeserializeFromTransaction()
            deserialize_from_transaction.deserialize(sender, instance, **kwargs)
        
