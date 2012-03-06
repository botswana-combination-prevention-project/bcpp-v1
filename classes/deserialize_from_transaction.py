from django.core import serializers
from django.db import IntegrityError
from transaction_producer import TransactionProducer

class DeserializeFromTransaction(object):

    def deserialize(self, sender, instance,**kwargs):
        
        incoming_transaction = instance
        
        for obj in serializers.deserialize("json",incoming_transaction.tx):
            # if you get an error deserializing a datetime, confirm dev version of json.py
            if incoming_transaction.action == 'I' or incoming_transaction.action == 'U':
                
                # deserialiser save() method
                # need to check if the model instance does not already exist as it may have been
                # auto-created by the CONSUMER on the save of the previous incoming_transaction.
                # Note that some incoming_transactions trigger the creation of new model instances on the consumer when their save() 
                # methods are called. (for example, saving a membership form triggers the creation of appointments)
                # this will cause an integrity error as the consumer will auto-create a model instance 
                # and the next incoming_transaction to be consumed will be that same model instance with a different pk.
                
                # get_by_natural_key_with_dict is disabled, just save()
                if 'xget_by_natural_key_with_dict' in dir(obj.object.__class__.objects):
                    if obj.object.__class__.objects.get_by_natural_key_with_dict(**obj.object.natural_key_as_dict()):
                        obj.object.pk = obj.object.__class__.objects.get_by_natural_key_with_dict(**obj.object.natural_key_as_dict()).pk
                        obj.save()
                    else:
                        raise TypeError('Cannot determine natural key of Serialized object %s using \'get_by_natural_key_with_dict\' method.' % (obj.object.__class__,) )
                else:  
                    # save using ModelBase save() method (skips all the subclassed save() methods)  
                    
                    try:
                        obj.save()
            
                        # call the object's save() method to trigger AuditTrail
                        # pass the producer so that new incoming_transactions on the
                        # consumer (self) correctly appear to come from the producer.
                        #if obj.object._meta.object_name.lower()[-5:] == 'audit':
                        #    obj.object.save()
                        #else:
                        #    obj.object.save(suppress_autocreate_on_deserialize=True)
                            
                        # POST success back to to the producer
                        incoming_transaction.is_consumed = True
                        incoming_transaction.consumer = str(TransactionProducer())
                        incoming_transaction.save()
                    except IntegrityError, err:
                        incoming_transaction.error = err
                    except: 
                        raise TypeError()    