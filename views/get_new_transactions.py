import urllib, urllib2, base64, socket
import simplejson as json
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime
from tastypie.models import ApiKey
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db import IntegrityError
from django.contrib import messages
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import serializers
from bhp_sync.models import Transaction, Producer, RequestLog
from bhp_sync.classes import TransactionProducer

@login_required
def get_new_transactions(request, **kwargs):

    if not 'ALLOW_MODEL_SERIALIZATION' in dir(settings):
        messages.add_message(request, messages.ERROR, 'ALLOW_MODEL_SERIALIZATION global boolean not found in settings.')                                                                                            
    
    producer = None
    if request.user:
        if 'api_key' in dir(request.user):
            if not request.user.api_key:
                raise ValueError, 'ApiKey not found for user %s. Perhaps run create_api_key().' % (request.user,)
            else:            
                #timeout = 10
                #socket_default_timeout = socket.getdefaulttimeout()        
                #consumed = []
                
                # specify producer "name" of the server you are connecting to 
                # as you only want transactions created by that server.
                producer = None
                if kwargs.get('producer'):
                    producer = Producer.objects.filter(name__iexact=kwargs.get('producer'))
                    if not producer:
                        messages.add_message(request, messages.ERROR, 'Unknown producer. Got %s.' % (kwargs.get('producer')))          
                    else:
                        producer = Producer.objects.get(name__iexact=kwargs.get('producer'))

                if producer:
                
                    # url to producer, add in the producer, username and api_key of the current user
                    data = {'host': producer.url, 'producer':producer.name, 'limit':producer.json_limit, 'username':request.user.username, 'api_key':request.user.api_key.key}
                    url = '{host}bhp_sync/api/transaction/?format=json&limit={limit}&producer={producer}&username={username}&api_key={api_key}'.format(**data)

                    request_log = RequestLog()
                    request_log.producer = producer
                    request_log.save()
                    
                    producer.sync_datetime = request_log.request_datetime
                    producer.sync_status = 'Error'
                    producer.save()
                    
                    err = None
                    req = urllib2.Request(url=url)
                    while req:
                        try:
                            f = urllib2.urlopen(req)
                            req = None
                        except urllib2.HTTPError, err:
                            request_log.status = 'error'
                            request_log.save()
                            req = None            
                            if err.code == 404:
                                messages.add_message(request, messages.ERROR, 'Unknown producer. Got %s.' % (kwargs.get('producer')))          
                        except urllib2.URLError, err:
                            producer.sync_status = 'error'                                                
                            request_log.status = 'error'
                            request_log.save()
                            messages.add_message(request, messages.ERROR, err)                                       
                            break

                        if not err:
                            # read response from url and decode          
                            response = f.read()
                            json_response = None
                            if response:
                                json_response =  json.loads(response)
                            
                                # response is limited to 20 objects, if there are more
                                # next will the the url with offset to fetch next 20 (&limit=20&offset=20)
                                if 'meta' in json_response:
                                    if json_response['meta']['next']:
                                        req = urllib2.Request(url=json_response['meta']['next'])
                                    if not json_response['meta']['total_count'] == 0:    
                                        messages.add_message(request, messages.INFO, 'Fetching. Limit is %s. Starting at %s of %s' % (json_response['meta']['limit'], json_response['meta']['offset'], json_response['meta']['total_count']) )                              
                                    producer.json_limit = json_response['meta']['limit']                                       
                                    producer.json_total_count = json_response['meta']['total_count']                                        
                                #except:
                                #    messages.add_message(request, messages.ERROR, 'Failed to decode response to JSON from %s URL %s.' % (producer.name,producer.url))  

                                if json_response:
                                    error_list = []
                                    messages.add_message(request, messages.INFO, 'Fetching %s unsent transactions from producer %s URL %s.' % (len(json_response['objects']), producer.name,url))                                                                                                    

                                    # 'transaction' is the serialized Transaction object from the producer. 
                                    # Recall that the Transaction's object field 'tx' has the serialized 
                                    # instance of the data model we are looking for
                                    for transaction in json_response['objects']:
                                        for obj in serializers.deserialize("json",transaction['tx']):
                                            # if you get an error deserializing a datetime, confirm dev version of json.py
                                            #try:
                                            if transaction['action'] == 'I' or transaction['action'] == 'U':
                                                
                                                # deserialiser save() method
                                                # need to check if the model instance does not already exist as it may have been
                                                # auto-created by the CONSUMER on the save of the previous transaction.
                                                # Note that some transactions trigger the creation of new model instances on the consumer when their save() 
                                                # methods are called. (for example, saving a membership form triggers the creation of appointments)
                                                # this will cause an integrity error as the consumer will auto-create a model instance 
                                                # and the next transaction to be consumed will be that same model instance with a different pk.
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
                                                obj.object.save(transaction_producer=transaction['producer'], suppress_autocreate_on_deserialize=True)
                                                
                                                # POST success back to to the producer
                                                transaction['is_consumed'] = True
                                                transaction['consumer'] = str(TransactionProducer())
                                                req = urllib2.Request(url, json.dumps(transaction, cls=DjangoJSONEncoder), {'Content-Type': 'application/json'})
                                                f = urllib2.urlopen(req)
                                                response = f.read()
                                                f.close()                        
                                                # display a message on the consumer (self)
                                                #messages.add_message(request, messages.SUCCESS, 'Import succeeded for %s' %(unicode(obj.object),))                                

                                            elif transaction['action'] == 'D':
                                                if 'ALLOW_DELETE_MODEL_FROM_SERIALIZATION' in dir(settings):
                                                    if settings.ALLOW_DELETE_MODEL_FROM_SERIALIZATION:
                                                        if obj.object.__class__.objects.filter(pk=transaction['tx_pk']):
                                                            obj_name = unicode(obj.object) 
                                                            obj.object.__class__.objects.get(pk=transaction['tx_pk']).delete(transaction_producer=transaction['producer'])
                                                            #messages.add_message(request, messages.SUCCESS, 'Delete succeeded for %s' %(obj_name,))                                            
                                                    else:
                                                        messages.add_message(request, messages.WARNING, 'Delete not allowed. %s' %(obj.object._meta.object_name,))
                                                        messages.add_message(request, messages.WARNING, 'Delete from imported serialized objects not allowed. See ALLOW_DELETE_MODEL_FROM_SERIALIZATION in settings.')                                                                                            
                                                else:
                                                    msg = 'ALLOW_DELETE_MODEL_FROM_SERIALIZATION global boolean not found in settings.'
                                                    messages.add_message(request, messages.ERROR, msg)                                                                                            
                                            else:
                                                raise ValueError, 'Unable to handle imported transaction, unknown \'action\'. Action must be I,U or D. Got %s' % (transaction['action'],)

        producer.sync_status = 'OK'
        producer.save()
        
    
        return render_to_response('new_transactions.html', { 
            'producer': producer,
        },context_instance=RequestContext(request))
