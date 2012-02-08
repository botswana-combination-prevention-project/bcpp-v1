from django.db.models import get_model
from transaction_producer import TransactionProducer

class SerializeToTransaction(object):

    def serialize(self, sender, instance,**kwargs):
        action = 'U'
        if kwargs.get('created'):
            action = 'I'
        transaction_producer = TransactionProducer()    
        Transaction = get_model('bhp_sync', 'transaction')

        use_natural_keys = False
        if 'natural_key' in dir(sender):
            use_natural_keys = True

        #if this is a proxy model, get to the main model
        if instance._meta.proxy_for_model:
            instance = instance._meta.proxy_for_model.objects.get(pk=instance.pk)

        json_tx = serializers.serialize("json", 
                        [instance,],
                        ensure_ascii=False, 
                        use_natural_keys=use_natural_keys)              
        Transaction.objects.create(
            tx_name = instance._meta.object_name,
            tx_pk = instance.pk,
            tx = json_tx,
            timestamp = datetime.today().strftime('%Y%m%d%H%M%S%f'),
            producer = str(transaction_producer),
            action = action,                
            )

