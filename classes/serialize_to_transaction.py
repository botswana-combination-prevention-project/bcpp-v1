from datetime import datetime
from django.db.models import get_model
from django.core import serializers
try:
    from bhp_crypto.classes import Crypter
except ImportError:
    pass
from transaction_producer import TransactionProducer

 
class SerializeToTransaction(object):

    def __init__(self, *args, **kwargs):
        super(SerializeToTransaction, self).__init__(*args, **kwargs)
        self.algorithm='aes'
        self.mode='aes-local'
        #self.set_private_key(self.get_local_rsa_private_keyfile())
        #self.set_aes_key()

    def serialize(self, sender, instance, **kwargs):
    
        """ Serialize the model instance to an encrypted json object and save the json object to the Transaction model. """
        
        """Transaction producer name is based on the hostname (created
        or modified) field.     
        
        Call this using the post_save and m2m_changed signal.
        
        For example, for models that inherit from BasicUuidModel

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

        # watch out for this. The producer is the device that created 
        # the "transaction" instance and not necessarily the one that created the model instance
        # so just using the hostname created or hostname modified would not necessarily work.
        action = 'U'
        if kwargs.get('created'):
            action = 'I'
        transaction_producer = TransactionProducer()
        #Transaction = get_model('bhp_sync', 'transaction')
        OutgoingTransaction = get_model('bhp_sync', 'outgoingtransaction')
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
        # Handle proxy models.
        # if this is a proxy model, get to the main model
        # Note, proxy model itself only returns a pointer to the
        # main model.
        # i do not want both the proxy model and its parent model to
        # trigger a transaction, but make sure the parent "model" has
        # is_serialized=True, otherwise no transaction will be created.
        if instance._meta.proxy_for_model:
            instance = instance._meta.proxy_for_model.objects.get(pk=instance.pk)
        # serialize to json
        # serialize everything? even those transactions you have just consumed?
        json_tx = serializers.serialize("json",
                        [instance, ],
                        ensure_ascii=False,
                        use_natural_keys=use_natural_keys)
        #aes encrypt the json_tx string
        try:
            crypter = Crypter()
            json_tx = crypter.encrypt(json_tx)
            del crypter
        except NameError:
            pass
        except AttributeError:
            pass
        # save to Outgoing Transaction.
        OutgoingTransaction.objects.create(
            tx_name=instance._meta.object_name,
            tx_pk=instance.pk,
            tx=json_tx,
            timestamp=datetime.today().strftime('%Y%m%d%H%M%S%f'),
            producer=str(transaction_producer),
            action=action,
            )
