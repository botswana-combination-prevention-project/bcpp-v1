from datetime import datetime
from django.db.models import get_model
from django.core import serializers
from bhp_crypto.classes import FieldCryptor
from transaction_producer import TransactionProducer


class SerializeToTransaction(object):

    def serialize(self, sender, instance, **kwargs):

        """ Serializes the model instance to an encrypted json object and saves the json object to the OutgoingTransaction model.

            Transaction producer name is based on the hostname (created or modified) field.

            Call this using the post_save and m2m_changed signal.
        """
        if not kwargs.get('raw', False):  # raw=True if you are saving a json object, maybe??
            using = kwargs.get('using', None)
            action = 'U'
            if kwargs.get('created'):
                action = 'I'
            transaction_producer = TransactionProducer()
            OutgoingTransaction = get_model('bhp_sync', 'outgoingtransaction')
            use_natural_keys = False
            if 'natural_key' in dir(sender):
                use_natural_keys = True
            # if this is a proxy model, get to the main model
            if instance._meta.proxy_for_model:
                instance = instance._meta.proxy_for_model.objects.get(pk=instance.pk)
            # serialize to json
            json_tx = serializers.serialize("json", [instance, ], ensure_ascii=False, use_natural_keys=use_natural_keys)
            try:
                # encrypt before saving to OutgoingTransaction
                json_tx = FieldCryptor('aes', 'local').encrypt(json_tx)
            except NameError:
                pass
            except AttributeError:
                pass
            except:
                raise
            return OutgoingTransaction.objects.using(using).create(
                tx_name=instance._meta.object_name,
                tx_pk=instance.pk,
                tx=json_tx,
                timestamp=datetime.today().strftime('%Y%m%d%H%M%S%f'),
                producer=str(transaction_producer),
                action=action)
