
import socket
from django.core import serializers
from django.db.utils import IntegrityError
from bhp_crypto.classes import FieldCrypter
from transaction_producer import TransactionProducer


class DeserializeFromTransaction(object):

    def __init__(self, *args, **kwargs):
        super(DeserializeFromTransaction, self).__init__(*args, **kwargs)

    def deserialize(self, sender, incoming_transaction, **kwargs):
        """ decrypt and deserialize the incoming json object"""

        for obj in serializers.deserialize("json", FieldCrypter(algorithm='aes', mode='local').decrypt(incoming_transaction.tx)):
        # if you get an error deserializing a datetime, confirm dev version of json.py
            if incoming_transaction.action == 'I' or incoming_transaction.action == 'U':
                # check if tx originanted from me
                #print "created %s : modified %s" % (obj.object.hostname_created, obj.object.hostname_modified)
                if obj.object.hostname_modified == socket.gethostname():
                    #print "Ignoring my own transaction %s" % (incoming_transaction.tx_pk)
                    pass
                else:
                    #print "deserializing %s" % (incoming_transaction.tx_pk)

                    # deserialiser save() method
                    # need to check if the model instance does not already exist as it may have been
                    # auto-created by the CONSUMER on the save of the previous incoming_transaction.
                    # Note that some incoming_transactions trigger the creation of new model instances on the consumer when their save()
                    # methods are called. (for example, saving a membership form triggers the creation of appointments)
                    # this will cause an integrity error as the consumer will auto-create a model instance
                    # and the next incoming_transaction to be consumed will be that same model instance with a different pk.

                    #  get_by_natural_key_with_dict is disabled, just save()
                    if 'DISABLEDget_by_natural_key_with_dict' in dir(obj.object.__class__.objects):
                        if obj.object.__class__.objects.get_by_natural_key_with_dict(**obj.object.natural_key_as_dict()):
                            obj.object.pk = obj.object.__class__.objects.get_by_natural_key_with_dict(**obj.object.natural_key_as_dict()).pk
                            obj.save()
                        else:
                            raise TypeError('Cannot determine natural key of Serialized object %s using \'get_by_natural_key_with_dict\' method.' % (obj.object.__class__,))
                    else:
                        try:
                            # save using ModelBase save() method (skips all the subclassed save() methods)
                            # post_save, etc signals will fire
                            obj.save()
                        except IntegrityError as error:
                            #print error
                            incoming_transaction.is_consumed = False
                            incoming_transaction.consumer = None
                            incoming_transaction.is_error = True
                            incoming_transaction.error = error
                            incoming_transaction.save()

                        except:
                            raise
                        else:
                            # POST success back to to the producer
                            incoming_transaction.is_consumed = True
                            incoming_transaction.consumer = str(TransactionProducer())
                            incoming_transaction.save()




