from django.conf import settings
 
from base_transaction import BaseTransaction
#try:

#except ImportError:
    #from django.conf import settings
#    if 'MQ' in dir(settings):
#        if settings.MQ:
#            import sys
#            sys.stderr.write("settings.MQ==True but couldn't find the bhp_mq.mq_producer_controller.py module.")
#            sys.exit(1)

class OutgoingTransaction(BaseTransaction):
    
    """ transactions produced locally to be consumed/sent to a queue or consumer """
    
    class Meta:
        app_label = 'bhp_sync'   
        ordering = ['timestamp']
        
        

        