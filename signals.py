#from datetime import datetime
##from django.db.models.signals import post_save #, m2m_changed
##from django.dispatch import receiver
#from django.core import serializers
#from django.db.models import get_model
#from django.contrib.auth.models import User
#from django.db import models
#from tastypie.models import create_api_key
##from bhp_common.models import MyBasicUuidModel
#from bhp_sync.classes import TransactionProducer
#
## tastypie signal to create api_ky
#models.signals.post_save.connect(create_api_key, sender=User)
#
#def json_to_transaction(sender, instance,**kwargs):
#    action = 'U'
#    if kwargs.get('created'):
#        action = 'I'
#    transaction_producer = TransactionProducer()    
#    transaction = get_model('bhp_sync', 'transaction')
#
#    use_natural_keys = False
#    if 'natural_key' in dir(sender):
#        use_natural_keys = True
#
#    #if this is a proxy model, get to the main model
#    if instance._meta.proxy_for_model:
#        instance = instance._meta.proxy_for_model.objects.get(pk=instance.pk)
#
#    json_tx = serializers.serialize("json", 
#                    [instance,],
#                    ensure_ascii=False, 
#                    use_natural_keys=use_natural_keys)              
#    
#    transaction.objects.create(
#        tx_name = instance._meta.object_name,
#        tx_pk = instance.pk,
#        tx = json_tx,
#        timestamp = datetime.today().strftime('%Y%m%d%H%M%S%f'),
#        producer = str(transaction_producer),
#        action = action,                
#        )
#
#"""
#@receiver(m2m_changed,)
#def serialize_m2m_on_save(sender, instance, **kwargs):
#    if kwargs.get('action') == 'post_add':
#        if isinstance(instance, MyBasicUuidModel):
#            if instance.is_serialized() and not instance._meta.proxy:
#                json_to_transaction(sender, instance,**kwargs)
#                   
#@receiver(post_save,)
#def serialize_on_save(sender, instance, **kwargs):
#    if isinstance(instance, MyBasicUuidModel):
#        if instance.is_serialized() and not instance._meta.proxy:
#            json_to_transaction(sender, instance,**kwargs)
#            
#"""
