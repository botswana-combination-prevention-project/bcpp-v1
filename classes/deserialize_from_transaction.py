#from datetime import datetime
from django.core import serializers
from transaction_producer import TransactionProducer


class DeserializeFromTransaction(object):

    def deserialize(self, sender, instance,**kwargs):
        
        transaction = instance
        obj = serializers.deserialize("json",transaction['tx'])
        
        # if you get an error deserializing a datetime, confirm dev version of json.py
        if transaction.action == 'I' or transaction.action == 'U':
            
            # deserialiser save() method
            # need to check if the model instance does not already exist as it may have been
            # auto-created by the CONSUMER on the save of the previous transaction.
            # Note that some transactions trigger the creation of new model instances on the consumer when their save() 
            # methods are called. (for example, saving a membership form triggers the creation of appointments)
            # this will cause an integrity error as the consumer will auto-create a model instance 
            # and the next transaction to be consumed will be that same model instance with a different pk.
            
            # get_by_natural_key_with_dict is disabled, just save()
            if 'xget_by_natural_key_with_dict' in dir(obj.object.__class__.objects):
                if obj.object.__class__.objects.get_by_natural_key_with_dict(**obj.object.natural_key_as_dict()):
                    obj.object.pk = obj.object.__class__.objects.get_by_natural_key_with_dict(**obj.object.natural_key_as_dict()).pk
                    obj.save()
                else:
                    raise TypeError('Cannot determine natural key of Serialized object %s using \'get_by_natural_key_with_dict\' method.' % (obj.object.__class__,) )
            else:    
                obj.save()
        
            # call the object's save() method to trigger AuditTrail
            # pass the producer so that new transactions on the
            # consumer (self) correctly appear to come from the producer.
            obj.object.save(suppress_autocreate_on_deserialize=True)
            #obj.object.save()
            
            # POST success back to to the producer
            transaction.is_consumed = True
            transaction.consumer = str(TransactionProducer())
            transaction.save()
