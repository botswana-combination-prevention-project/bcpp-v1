from datetime import datetime
from django.db.models import get_model
from django.core import serializers
from transaction_producer import TransactionProducer

class SerializeToTransaction(object):

    def serialize(self, sender, instance,**kwargs):
    
        """Serialize the model instance to a json object and 
        save the json object to the Transaction model.
        
        Transaction producer name is based on the hostname (created
        or modified) field. 
        
        Call this using the post_save and m2m_changed signal.
        
        For example, for models that inherit from MyBasicUuidModel

            @receiver(m2m_changed,)
            def serialize_m2m_on_save(sender, instance, **kwargs):
                if kwargs.get('action') == 'post_add':
                    if isinstance(instance, MyBasicUuidModel):
                        if instance.is_serialized() and not instance._meta.proxy:
                            serialize_to_transaction = SerializeToTransaction()
                            serialize_to_transaction.serialize(sender, instance,**kwargs)
                               
            @receiver(post_save,)
            def serialize_on_save(sender, instance, **kwargs):
                if isinstance(instance, MyBasicUuidModel):
                    if instance.is_serialized() and not instance._meta.proxy:
                        serialize_to_transaction = SerializeToTransaction()
                        serialize_to_transaction.serialize(sender, instance,**kwargs)
        """

        action = 'U'
        hostname = instance.hostname_modified
        if kwargs.get('created'):
            action = 'I'
            hostname = instance.hostname_created
        if not hostname:
            hostname = instance.hostname_created
        transaction_producer = TransactionProducer(hostname=hostname)    
        Transaction = get_model('bhp_sync', 'transaction')

        # 'suppress_autocreate_on_deserialize' is passed by the method that
        # deserializes a transaction to avoid duplicating autocreated related model instances. 
        # The conditional was used in the save method of the model that was saved. 
        # It can (and must) now be discarded.
        if 'suppress_autocreate_on_deserialize' in dir(sender):
            del kwargs['suppress_autocreate_on_deserialize']

        # TODO: is there value in using this??
        use_natural_keys = False
        if 'natural_key' in dir(sender):
            use_natural_keys = True

        # if this is a proxy model, get to the main model
        # Note, proxy model itself only returns a pointer to the 
        # main model.
        if instance._meta.proxy_for_model:
            instance = instance._meta.proxy_for_model.objects.get(pk=instance.pk)

        # serialize to json
        json_tx = serializers.serialize("json", 
                        [instance,],
                        ensure_ascii = False, 
                        use_natural_keys = use_natural_keys)              

        # save to Transaction.
        Transaction.objects.create(
            tx_name = instance._meta.object_name,
            tx_pk = instance.pk,
            tx = json_tx,
            timestamp = datetime.today().strftime('%Y%m%d%H%M%S%f'),
            producer = str(transaction_producer),
            action = action,                
            )

