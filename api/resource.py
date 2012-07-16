#from tastypie import fields
from tastypie.serializers import Serializer
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
#from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from bhp_sync.models import OutgoingTransaction

"""
from django.contrib.auth.models import User
from django.db import models
from tastypie.models import create_api_key
for user in User.objects.all():
    if not ApiKey.objects.filter(user=user):
        create_api_key(instance=user, created=True)
        
from django.contrib.auth.models import User
from django.db import models
from tastypie.models import create_api_key
for user in User.objects.all():
    if not ApiKey.objects.filter(user=user):
        ApiKey.objects.create(user=user)
        
api_key = ApiKey.objects.get(user=User.objects.get(username='erikvw'))
api_key.key='1af87bd7d0c7763e7b11590c9398740f0de7678b'
api_key.save()
        
api_key = ApiKey.objects.get(user=User.objects.get(username='kbinda'))
api_key.key='0a0b09212e2661d01b09ffe2c780145dc86c1cd6'
api_key.save()  

api_key = ApiKey.objects.get(user=User.objects.get(username='tlentswe'))
api_key.key='93d15e5d8b8c589c28be956a4419d18c5c657924'
api_key.save()
    
        
"""    


class OutgoingTransactionResource(ModelResource):
    
    """ APi resource based on model OutgoingTransaction filtered on is_consumed=False. """
    
    class Meta:
        queryset=OutgoingTransaction.objects.filter(is_consumed=False).order_by('timestamp')
        resource_name='outgoingtransaction'
        authentication=ApiKeyAuthentication()
        authorization=DjangoAuthorization()       
        allowed_methods=['get','post','put',]        
        filtering={
            'producer': ['exact',],
        }        
        serializer=Serializer()
        

#models.signals.post_save.connect(create_api_key, sender=User)
