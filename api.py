from tastypie import fields
from tastypie.serializers import Serializer
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS, ALL
from models import Transaction

"""
TODO : ApiKeyAuthentication
"""


class TransactionResource(ModelResource):
    class Meta:
        queryset = Transaction.objects.filter(is_sent=False)
        resource_name = 'transaction'
        #authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()       
        #authorization = Authorization()         
        #excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        allowed_methods = ['get','post','put',]        
        filtering = {
            'producer': ['exact',],
        }        serializer = Serializer()

