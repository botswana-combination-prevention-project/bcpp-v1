from datetime import datetime
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.conf import settings
from django.core import serializers
from django.db.models import get_model
from bhp_common.models import MyBasicModel
from bhp_common.fields import MyUUIDField
from bhp_sync.classes import TransactionProducer
from bhp_sync.decorators import receiver_subclasses

class MyBasicUuidModel(MyBasicModel):

    """Base model class for all models using an UUID and not an INT for the primary key. """
    
    id = MyUUIDField(primary_key=True)

    def is_serialized(self, serialize=False):

        if 'ALLOW_MODEL_SERIALIZATION' in dir(settings):
            if settings.ALLOW_MODEL_SERIALIZATION:
                return serialize
        return False
        
    def save(self, *args, **kwargs):
    
        # sneek in the transaction_producer, if called from 
        # view in bhp_sync.
        # get value and delete from kwargs before calling super
        transaction_producer = TransactionProducer()
        if 'transaction_producer' in kwargs:
            transaction_producer = kwargs.get('transaction_producer')            
            del kwargs['transaction_producer']

        super(MyBasicUuidModel, self).save(*args, **kwargs)
        
        # note that i do not want both the proxy model and its parent model to 
        # trigger a transaction, but make sure the parent "model" has
        # is_serialized=True, otherwise no transaction will be created.

        if self.pk and self.is_serialized(): #and not self._meta.proxy:

            action = 'I'
            if self.pk:
                action = 'U'
            
            transaction = get_model('bhp_sync', 'transaction')
            use_natural_keys = False
            if 'natural_key' in dir(self):
                use_natural_keys = True
            json_tx = serializers.serialize("json", 
                            self.__class__.objects.filter(pk=self.pk),
                            ensure_ascii=False, 
                            use_natural_keys=use_natural_keys)            
            transaction.objects.create(
                tx_name = self._meta.object_name,
                tx_pk = self.pk,
                tx = json_tx,
                timestamp = datetime.today().strftime('%Y%m%d%H%M%S%f'),
                producer = str(transaction_producer),
                action = action,                
                )
            #messages.add_message('', messages.SUCCESS, 'Successfully serialized %s for producer %s' %(unicode(self),str(transaction_producer)))                                                            
 
    def delete(self, *args, **kwargs):

        #TODO: get this to work in pre_delete signal
        transaction_producer = TransactionProducer()    
        if 'transaction_producer' in kwargs:
            transaction_producer = kwargs.get('transaction_producer')            
            del kwargs['transaction_producer']

        if self.is_serialized() and not self._meta.proxy:

            transaction = get_model('bhp_sync', 'transaction')
            json_obj = serializers.serialize("json", self.__class__.objects.filter(pk=self.pk), )            
            transaction.objects.create(
                tx_name = self._meta.object_name,
                tx_pk = self.pk,
                tx = json_obj,
                timestamp = datetime.today().strftime('%Y%m%d%H%M%S%f'),
                producer = str(transaction_producer),
                action = 'D',
                )
        super(MyBasicUuidModel, self).delete(*args, **kwargs)


    class Meta:
        abstract = True
"""        
@receiver_subclasses(pre_delete, MyBasicUuidModel, "mybasicuuidmodel_pre_delete")
def serialize_on_delete(sender, instance, **kwargs):
    if instance.is_serialized() and not instance._meta.proxy:
        transaction_producer = TransactionProducer()    
        transaction = get_model('bhp_sync', 'transaction')
        json = serializers.serialize("json", instance.__class__.objects.filter(pk=instance.pk), )            
        transaction.objects.create(
            tx_name = instance._meta.object_name,
            tx_pk = instance.pk,
            tx = json,
            timestamp = datetime.today().strftime('%Y%m%d%H%M%S%f'),
            producer = str(transaction_producer),
            action = 'D',
            )
"""

