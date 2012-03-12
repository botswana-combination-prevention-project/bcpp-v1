from django.db.models.signals import post_save
from django.dispatch import receiver 
from base_transaction import BaseTransaction
from bhp_mq.classes import mq_producer_controller


class OutgoingTransaction(BaseTransaction):
    
    """ transactions produced locally to be consumed/sent to a queue or consumer """
    
    class Meta:
        app_label = 'bhp_sync'   
        ordering = ['timestamp']
        
        
@receiver(post_save, sender=OutgoingTransaction,  dispatch_uid="send_to_mq_on_post_save")
def send_to_mq_on_post_save(sender, instance, **kwargs):
    if isinstance(instance, OutgoingTransaction):
        if not instance.is_consumed and not instance.is_error:
            mq_producer_controller.send_message(instance)
        