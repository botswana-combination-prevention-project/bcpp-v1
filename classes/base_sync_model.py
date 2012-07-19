from datetime import datetime
from django.conf import settings
from django.core import serializers
from django.db.models import get_model
from bhp_sync.classes import TransactionProducer
from bhp_base_model.classes import BaseUuidModel
#from bhp_bucket.classes.bucket_controller import bucket


class BaseSyncModel(BaseUuidModel):

    """ Base model for all UUID models and adds synchronization methods and signals. """

    def is_serialized(self, serialize=True):

        if 'ALLOW_MODEL_SERIALIZATION' in dir(settings):
            if settings.ALLOW_MODEL_SERIALIZATION:
                return serialize
        return False
    
    def save(self, *args, **kwargs):
        
        # sneek in the transaction_producer, if called from 
        # view in bhp_sync.
        # get value and delete from kwargs before calling super
        #transaction_producer = TransactionProducer()
        if 'transaction_producer' in kwargs:
            #transaction_producer = kwargs.get('transaction_producer')            
            del kwargs['transaction_producer']
        
        # used 'suppress_autocreate_on_deserialize' to not allow save methods
        # to create new model instances such as appointments, ScheduledEntry, etc
        # as these will be serialized on the producer
        if 'suppress_autocreate_on_deserialize' in kwargs:
            del kwargs['suppress_autocreate_on_deserialize']

        super(BaseSyncModel, self).save(*args, **kwargs)
                 
    def delete(self, *args, **kwargs):

        #TODO: get this to work in pre_delete signal
        transaction_producer = TransactionProducer()    
        if 'transaction_producer' in kwargs:
            transaction_producer = kwargs.get('transaction_producer')            
            del kwargs['transaction_producer']

        if self.is_serialized() and not self._meta.proxy:

            transaction = get_model('bhp_sync', 'transaction')
            json_obj = serializers.serialize(
                "json", self.__class__.objects.filter(pk=self.pk), use_natural_keys=True )            
            transaction.objects.create(
                tx_name = self._meta.object_name,
                tx_pk = self.pk,
                tx = json_obj,
                timestamp = datetime.today().strftime('%Y%m%d%H%M%S%f'),
                producer = str(transaction_producer),
                action = 'D',
                )
        super(BaseSyncModel, self).delete(*args, **kwargs)


    class Meta:
        abstract = True


