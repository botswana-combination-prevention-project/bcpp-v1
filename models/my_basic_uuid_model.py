from datetime import datetime
#from django.db.models.signals import pre_delete
#from django.dispatch import receiver
from django.conf import settings
from django.core import serializers
from django.db.models import get_model
from bhp_common.models import MyBasicModel
from bhp_common.fields import MyUUIDField
from bhp_sync.classes import TransactionProducer

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
        
        if self.pk and self.is_serialized() and not self._meta.proxy:

            action = 'I'
            if self.pk:
                action = 'U'
                
            transaction = get_model('bhp_sync', 'transaction')
            json = serializers.serialize("json", self.__class__.objects.filter(pk=self.pk), )            
            transaction.objects.create(
                tx_name = self._meta.object_name,
                tx_pk = self.pk,
                tx = json,
                timestamp = datetime.today().strftime('%Y%m%d%H%M%S%f'),
                producer = str(transaction_producer),
                action = action,                
                )
 
    def delete(self, *args, **kwargs):

        transaction_producer = TransactionProducer()    
        if 'transaction_producer' in kwargs:
            transaction_producer = kwargs.get('transaction_producer')            
            del kwargs['transaction_producer']

        if self.is_serialized() and not self._meta.proxy:

            transaction = get_model('bhp_sync', 'transaction')
            json = serializers.serialize("json", self.__class__.objects.filter(pk=self.pk), )            
            transaction.objects.create(
                tx_name = self._meta.object_name,
                tx_pk = self.pk,
                tx = json,
                timestamp = datetime.today().strftime('%Y%m%d%H%M%S%f'),
                producer = str(transaction_producer),
                action = 'D',
                )
        super(MyBasicUuidModel, self).delete(*args, **kwargs)
    
    class Meta:
        abstract = True
        
#@receiver(pre_delete, sender=MyBasicUuidModel)
#def serialize_on_delete(sender, **kwargs):
#    raise TypeError()
#    if self.pk and self.is_serialized() and not self._meta.proxy:
#
#        transaction = get_model('bhp_sync', 'transaction')
#        json = serializers.serialize("json", self.__class__.objects.filter(pk=self.pk), )            
#        transaction.objects.create(
#            tx_name = self._meta.object_name,
#            tx_pk = self.pk,
#            tx = json,
#            timestamp = datetime.today().strftime('%Y%m%d%H%M%S%f'),
#            producer = transaction_producer,
#            action = 'D',
#            )

