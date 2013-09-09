import socket
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from bhp_sync.classes import SerializeToTransaction
from incoming_transaction import IncomingTransaction
from middle_man_transaction import MiddleManTransaction
from base_sync_uuid_model import BaseSyncUuidModel

@receiver(post_save, weak=False, dispatch_uid="deserialize_to_inspector_on_post_save")
def deserialize_to_inspector_on_post_save(sender, instance, **kwargs):
    if isinstance(instance, MiddleManTransaction):
        instance.deserialize_to_inspector_on_post_save(**kwargs)
        
@receiver(m2m_changed, weak=False, dispatch_uid='serialize_m2m_on_save')
def serialize_m2m_on_save(sender, instance, **kwargs):
    """ Part of the serialize transaction process that ensures m2m are
    serialized correctly.
    """
    if kwargs.get('action') == 'post_add':
        if isinstance(instance, BaseSyncUuidModel):
            if instance.is_serialized() and not instance._meta.proxy:
                serialize_to_transaction = SerializeToTransaction()
                serialize_to_transaction.serialize(sender, instance, **kwargs)


@receiver(post_save, weak=False, dispatch_uid='serialize_on_save')
def serialize_on_save(sender, instance, **kwargs):
    """ Serialize the model instance to the outgoing transaction
    model for consumption by another application.
    """
    if isinstance(instance, BaseSyncUuidModel):
        hostname = socket.gethostname()
        if (instance.hostname_created == hostname and not instance.hostname_modified) or (instance.hostname_modified == hostname):
            if instance.is_serialized() and not instance._meta.proxy:
                serialize_to_transaction = SerializeToTransaction()
                serialize_to_transaction.serialize(sender, instance, **kwargs)


@receiver(post_save, sender=IncomingTransaction, dispatch_uid="deserialize_on_post_save")
def deserialize_on_post_save(sender, instance, **kwargs):
    pass
    """ Callback to deserialize an incoming transaction.

    as long as the transaction is not consumed or in error"""

#    if isinstance(instance, IncomingTransaction):
#        if not instance.is_consumed and not instance.is_error:  # and not instance.is_self:
#            deserialize_from_transaction = DeserializeFromTransaction()
#            try:
#                deserialize_from_transaction.deserialize_from_signal(sender, instance, **kwargs)
#            except:
#                pass
