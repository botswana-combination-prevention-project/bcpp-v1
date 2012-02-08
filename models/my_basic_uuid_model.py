from datetime import datetime
from django.conf import settings
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core import serializers
from django.db.models import get_model
from bhp_common.models import MyBasicModel
from bhp_common.fields import MyUUIDField
from bhp_sync.classes import TransactionProducer, SerializeToTransaction


class MyBasicUuidModel(MyBasicModel):

    """Base model class for all models using an UUID and not an INT for the primary key. """
    
    id = MyUUIDField(primary_key=True)

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
        
        # use 'suppress_autocreate_on_deserialize' to not allow save methods
        # to create new model instances such as appointments, ScheduledEntry, etc
        # as these will be serialized on the producer
        if 'suppress_autocreate_on_deserialize' in kwargs:
            del kwargs['suppress_autocreate_on_deserialize']
            
        action = 'I'
        if self.pk:
            action = 'U'

        super(MyBasicUuidModel, self).save(*args, **kwargs)
        
        # note that i do not want both the proxy model and its parent model to 
        # trigger a transaction, but make sure the parent "model" has
        # is_serialized=True, otherwise no transaction will be created.

        """
        if self.pk and self.is_serialized():
            transaction = get_model('bhp_sync', 'transaction')
            use_natural_keys = False
            if 'natural_key' in dir(self):
                use_natural_keys = Truefrom django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
            #if this is a proxy model, get to the main model
            if self._meta.proxy_for_model:
                obj = self._meta.proxy_for_model.objects.get(pk=self.pk)
            else:
                obj = self    
            #if self.__class__._meta.object_name.lower() == 'qn002sectionone':
            #    raise TypeError(self.__dict__)    
            json_tx = serializers.serialize("json", 
                            obj.__class__.objects.filter(pk=obj.pk),
                            ensure_ascii=False, 
                            use_natural_keys=use_natural_keys)            
            transaction.objects.create(
                tx_name = obj._meta.object_name,
                tx_pk = obj.pk,
                tx = json_tx,
                timestamp = datetime.today().strftime('%Y%m%d%H%M%S%f'),
                producer = str(transaction_producer),
                action = action,                
                )
        """            
         
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
        super(MyBasicUuidModel, self).delete(*args, **kwargs)


    class Meta:
        abstract = True


@receiver(m2m_changed,)
def serialize_m2m_on_save(sender, instance, **kwargs):
    if kwargs.get('action') == 'post_add':
        if isinstance(instance, MyBasicUuidModel):
            if instance.is_serialized() and not instance._meta.proxy:
                serialize_to_transaction = SerializeToTransaction()
                serialize_to_transaction.serialize(sender, instance,**kwargs)
                   
@receiver(post_save,)
def serialize_on_save(sender, instance, **kwargs):
    if isinstance(instance, MyBasicUuidModel):
        if instance.is_serialized() and not instance._meta.proxy:
            serialize_to_transaction = SerializeToTransaction()
            serialize_to_transaction.serialize(sender, instance,**kwargs)




