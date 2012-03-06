from base_transaction import BaseTransaction


class OutgoingTransaction(BaseTransaction):
    
    """ transactions produced locally to be consumed/sent to a queue or consumer """
    
    class Meta:
        app_label = 'bhp_sync'   
        ordering = ['timestamp']