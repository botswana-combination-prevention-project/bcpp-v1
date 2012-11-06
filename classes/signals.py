import socket
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from serialize_to_transaction import SerializeToTransaction
from base_sync_model import BaseSyncModel


@receiver(m2m_changed, weak=False, dispatch_uid='serialize_m2m_on_save')
def serialize_m2m_on_save(sender, instance, **kwargs):
    """ Part of the serialize transaction process that ensures m2m are serialized correctly."""
    if kwargs.get('action') == 'post_add':
        if isinstance(instance, BaseSyncModel):
            if instance.is_serialized() and not instance._meta.proxy:
                serialize_to_transaction = SerializeToTransaction()
                serialize_to_transaction.serialize(sender, instance, **kwargs)


@receiver(post_save, weak=False, dispatch_uid='serialize_on_save')
def serialize_on_save(sender, instance, **kwargs):
    """ Serialize the model instance to the outgoing transaction model for consumption by another application. """
    if isinstance(instance, BaseSyncModel):
        hostname = socket.gethostname()
        if (instance.hostname_created == hostname and not instance.hostname_modified) or (instance.hostname_modified == hostname):
            if instance.is_serialized() and not instance._meta.proxy:
                serialize_to_transaction = SerializeToTransaction()
                serialize_to_transaction.serialize(sender, instance, **kwargs)

