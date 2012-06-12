#from datetime import datetime
#from django.conf import settings
#from django.db.models.signals import post_save, m2m_changed
#from django.dispatch import receiver
#from django.core import serializers
#from django.db.models import get_model
#from bhp_sync.classes import TransactionProducer, SerializeToTransaction
#from bhp_bucket.classes.bucket_controller import bucket
#from bhp_base_model.classes import BaseUuidModel
#
#
#class MyBasicUuidModel(BaseUuidModel):
#
#    """Base model class for all models using an UUID and not an INT for the primary key. """
#
#    def is_serialized(self, serialize=True):
#
#        if 'ALLOW_MODEL_SERIALIZATION' in dir(settings):
#            if settings.ALLOW_MODEL_SERIALIZATION:
#                return serialize
#        return False
#        
#    def save(self, *args, **kwargs):
#
#        # sneek in the transaction_producer, if called from 
#        # view in bhp_sync.
#        # get value and delete from kwargs before calling super
#        #transaction_producer = TransactionProducer()
#        if 'transaction_producer' in kwargs:
#            #transaction_producer = kwargs.get('transaction_producer')            
#            del kwargs['transaction_producer']
#        
#        # used 'suppress_autocreate_on_deserialize' to not allow save methods
#        # to create new model instances such as appointments, ScheduledEntry, etc
#        # as these will be serialized on the producer
#        if 'suppress_autocreate_on_deserialize' in kwargs:
#            del kwargs['suppress_autocreate_on_deserialize']
#
#        super(MyBasicUuidModel, self).save(*args, **kwargs)
#                 
#    def delete(self, *args, **kwargs):
#
#        #TODO: get this to work in pre_delete signal
#        transaction_producer = TransactionProducer()    
#        if 'transaction_producer' in kwargs:
#            transaction_producer = kwargs.get('transaction_producer')            
#            del kwargs['transaction_producer']
#
#        if self.is_serialized() and not self._meta.proxy:
#
#            transaction = get_model('bhp_sync', 'transaction')
#            json_obj = serializers.serialize(
#                "json", self.__class__.objects.filter(pk=self.pk), use_natural_keys=True )            
#            transaction.objects.create(
#                tx_name = self._meta.object_name,
#                tx_pk = self.pk,
#                tx = json_obj,
#                timestamp = datetime.today().strftime('%Y%m%d%H%M%S%f'),
#                producer = str(transaction_producer),
#                action = 'D',
#                )
#        super(MyBasicUuidModel, self).delete(*args, **kwargs)
#
#
#    class Meta:
#        abstract = True
#
#""" Signals """
#
#
#
#@receiver(m2m_changed, weak=False, dispatch_uid='serialize_m2m_on_save')
#def serialize_m2m_on_save(sender, instance, **kwargs):
#    """ part of the serialize transaction process that ensures m2m are serialized correctly """
#    if kwargs.get('action') == 'post_add':
#        if isinstance(instance, MyBasicUuidModel):
#            if instance.is_serialized() and not instance._meta.proxy:
#                serialize_to_transaction = SerializeToTransaction()
#                serialize_to_transaction.serialize(sender, instance,**kwargs)
#                   
#@receiver(post_save, weak=False, dispatch_uid='serialize_on_save')
#def serialize_on_save(sender, instance, **kwargs):
#    """ serialize the model instance to the outgoing transaction model for consumption by another application """
#    if isinstance(instance, MyBasicUuidModel):
#        if instance.is_serialized() and not instance._meta.proxy:
#            serialize_to_transaction = SerializeToTransaction()
#            serialize_to_transaction.serialize(sender, instance,**kwargs)
#
#@receiver(post_save, weak=False, dispatch_uid='model_bucket_rules_on_save' )
#def model_bucket_rules_on_save(sender, instance, **kwargs):
#    """ update / run model bucket rules, see bhp_bucket """
#    if isinstance(instance, MyBasicUuidModel):
#        bucket.update(instance)
