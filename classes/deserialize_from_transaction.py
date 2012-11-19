import sys
import socket
from django.core import serializers
from django.db.models import ForeignKey, get_model
from django.db.utils import IntegrityError
from bhp_crypto.classes import FieldCryptor
from transaction_producer import TransactionProducer


class DeserializeFromTransaction(object):

    def __init__(self, *args, **kwargs):
        super(DeserializeFromTransaction, self).__init__(*args, **kwargs)

    def deserialize_from_signal(self, sender, incoming_transaction, **kwargs):
        """ decrypt and deserialize the incoming json object"""
        allow = True
        Dispatch = get_model('bhp_dispatch', 'HbcDispatch')
        if Dispatch:
            if not Dispatch.objects.filter(producer=incoming_transaction.producer):
                allow = False
        if allow:
            self.deserialize(incoming_transaction)

    def deserialize(self, incoming_transaction):

        for obj in serializers.deserialize("json", FieldCryptor('aes', 'local').decrypt(incoming_transaction.tx)):
        # if you get an error deserializing a datetime, confirm dev version of json.py
            if incoming_transaction.action == 'I' or incoming_transaction.action == 'U':
                # check if tx originanted from me
                #print "created %s : modified %s" % (obj.object.hostname_created, obj.object.hostname_modified)
                incoming_transaction.is_ignored = False
                print '    {0}'.format(obj.object)
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
                        is_success = False
                        try:
                            # save using ModelBase save() method (skips all the subclassed save() methods)
                            # post_save, etc signals will fire
                            if 'deserialize_prep' in dir(obj.object):
                                # if there is anything special you wish to do to change on the instance
                                # override this method on your model
                                obj.object.deserialize_prep()
                            try:
                                # force insert even if it is an update
                                # to trigger an integrity error if it is an update
                                obj.save(force_insert=True)
                                print '    OK on force insert'
                                is_success = True
                            except:
                                # insert failed so unique contraints blocked the forced insert above
                                # check if there is a helper method
                                print '    force insert failed'
                                if 'deserialize_on_duplicate' in dir(obj.object):
                                    obj.object.deserialize_on_duplicate()
                                    obj.save()
                                    print '    OK update succeeded after deserialize_on_duplicate'
                                    is_success = True
                                else:
                                    obj.save()
                                    print '    OK update succeeded as is'
                                    is_success = True
                        except IntegrityError as error:
                            # failed both insert and update, why?
                            print '    integrity error'
                            if 'Cannot add or update a child row' in error.args[1]:
                                # which foreign key is failing?
                                if 'audit' in obj.object._meta.db_table:
                                    # audit tables do not have access to the helper methods
                                    #for field in foreign_key_error:
                                    #    # it is OK to just set the fk to None
                                    #    setattr(obj.object, field.name, None)
                                    print '    audit instance, ignoring...'
                                    incoming_transaction.is_ignored = True
                                else:
                                    foreign_key_error = []
                                    for field in obj.object._meta.fields:
                                        if isinstance(field, ForeignKey):
                                            try:
                                                getattr(obj.object, field.name)
                                            except:
                                                print '    unable to getattr {0}'.format(field.name)
                                                foreign_key_error.append(field)
                                    for field in foreign_key_error:
                                        print '    deserialize_get_missing_fk on model {0} for field {1}'.format(obj.object._meta.object_name, field.name)
                                        setattr(obj.object, field.name, obj.object.deserialize_get_missing_fk(field.name))
                                    try:
                                        obj.save()
                                        print '   OK saved after integrity error'
                                        is_success = True
                                    except:
                                        incoming_transaction.is_ignored = True
                            elif 'Duplicate' in error.args[1]:
                                # if the integrity error refers to a duplicate
                                # check the unique_together meta class value to attempt to
                                # locate the existing pk.
                                # If pk found, overwrite the pk in the json with the existing pk.
                                # Try to save again
                                print '    duplicate'
                                if not obj.object._meta.unique_together:
                                    # if there is no other constraint on the model
                                    # then an integrity error does not really make sense.
                                    # but anyway ...
                                    print '   missing unique_together attribute'
                                    raise
                                options = {}
                                for tpl in obj.object._meta.unique_together:
                                    for f in tpl:
                                        options.update({f: getattr(obj.object, f)})
                                    if not obj.object.__class__.objects.filter(**options).exists():
                                        # it should exist, otherwise how did we get an integrity error?
                                        print '   not found using unique_together field atttributes'
                                        raise
                                    else:
                                        old_pk = obj.object.id
                                        new_pk = obj.object.__class__.objects.get(**options).pk
                                        obj.object.id = new_pk
                                        try:
                                            print '    deserialize_on_duplicate'
                                            if 'deserialize_on_duplicate' in dir(obj.object):
                                                print '    deserialize_on_duplicate'
                                                obj.object.deserialize_on_duplicate()
                                                # not every duplicate needs to be saved
                                                # if you can develop criteria to decide,
                                                # then use deserialize_on_duplicate to evaluate
                                                print '    try save again'
                                                obj.save()
                                                is_success = True
                                                # change all pk to the new pk for is_consumed=False.
                                                print '    OK saved, now replace_pk_in_tx'
                                                incoming_transaction.__class__.objects.replace_pk_in_tx(old_pk, new_pk)
                                                print '    {0} is now {1}'.format(old_pk, new_pk)
                                            else:
                                                print '    no deserialize_on_duplicate method'
                                                incoming_transaction.is_ignored = True
                                        except IntegrityError as error:
                                            print '    integrity error ... giving up.'
                                            incoming_transaction.is_consumed = False
                                            incoming_transaction.consumer = None
                                            incoming_transaction.is_error = True
                                            incoming_transaction.error = error
                                            incoming_transaction.save()
                                        except:
                                            print "        [a] Unexpected error:", sys.exc_info()[0]
                                            raise
                            else:
                                print '    {0}'.format(error)
                                raise
                        except:
                            print "        [b] Unexpected error:", sys.exc_info()
                            raise
                        if is_success:
                            incoming_transaction.is_consumed = True
                            incoming_transaction.consumer = str(TransactionProducer())
                            incoming_transaction.save()
