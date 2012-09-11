from django.db.models.signals import post_save
from django.dispatch import receiver

from bhp_sync.classes import DeserializeFromTransaction
from incoming_transaction import IncomingTransaction


@receiver(post_save, sender=IncomingTransaction, dispatch_uid="deserialize_on_post_save")
def deserialize_on_post_save(sender, instance, **kwargs):

    """ Callback to deserialize an incoming transaction.

    as long as the transaction is not consumed or in error"""

    if isinstance(instance, IncomingTransaction):
        if not instance.is_consumed and not instance.is_error:  # and not instance.is_self:
            deserialize_from_transaction = DeserializeFromTransaction()
            try:
                deserialize_from_transaction.deserialize(sender, instance, **kwargs)
            except:
                pass
