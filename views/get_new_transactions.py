import urllib2, base64, socket
import simplejson as json
from datetime import datetime
from tastypie.models import ApiKey
from django.contrib.auth.models import User
from django.conf import settings
from django.db import IntegrityError
from django.contrib import messages
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import serializers
from bhp_sync.models import Transaction, Producer, RequestLog
from bhp_sync.classes import TransactionProducer


def get_new_transactions(request, **kwargs):

    if not 'ALLOW_MODEL_SERIALIZATION' in dir(settings):
        messages.add_message(request, messages.ERROR, 'ALLOW_MODEL_SERIALIZATION global boolean not found in settings.')                                                                                            
    
    if not request.user.api_key:
        raise ValueError, 'ApiKey not found for user %s. Perhaps run create_api_key().' % (request.user,)
                
    timeout = 5
    socket_default_timeout = socket.getdefaulttimeout()        
    consumed = []
    
    # specify producer "name" of the server you are connecting to 
    # as you only want transactions created by that server.
    if kwargs.get('producer'):
        producers = Producer.objects.filter(name__iexact=kwargs.get('producer'))
        if not producers:
            messages.add_message(request, messages.ERROR, 'Unknown producer. Got %s.' % (kwargs.get('producer')))          
    else:
        producers = Producer.objects.all()

    # producers is usually only one producer instance
    for producer in producers:
        # url to producer, add in the producer, username and api_key of the current user
        url = '%s?producer=%s&username=%s&api_key=%s' % (producer.url, producer.name, request.user.username, request.user.api_key.key)
        request_log = RequestLog()
        request_log.producer = producer
        request_log.save()
        
        try:
            f = urllib2.urlopen(url)
        except urllib2.HTTPError, err:
            if err.code == 404:
                messages.add_message(request, messages.ERROR, 'Unknown producer. Got %s.' % (kwargs.get('producer')))          
                break
            else:
                raise urllib2.HTTPError(err) 
        
        # read response from url and decode          
        response = f.read()
        json_response = None
        try:
            json_response =  json.loads(response)   
        except:   
            messages.add_message(request, messages.ERROR, 'Failed to decode response to JSON from %s URL %s.' % (producer.name,producer.url))  

        if json_response:
            error_list = []
            messages.add_message(request, messages.INFO, 'Fetching %s unsent transactions from producer %s URL %s.' % (len(json_response['objects']), producer.name,url))                                                                                                    

            # 'transaction' is the serialized Transaction object from the producer. 
            # Recall that the Transaction's object field 'tx' has the serialized 
            # instance of the data model we are looking for
            for transaction in json_response['objects']:
                for obj in serializers.deserialize("json",transaction['tx']):
                    #try:
                    if transaction['action'] == 'I' or transaction['action'] == 'U':
                        # deserialiser save() method
                        obj.save()
                        # call the object's save() method to trigger AuditTrail
                        # pass the producer so that new transactions on the
                        # consumer (self) correctly appear to come from the producer.
                        obj.object.save(transaction_producer=transaction['producer'])
                        # POST success back to to the producer
                        transaction['is_consumed'] = True
                        transaction['consumer'] = str(TransactionProducer())
                        req = urllib2.Request(url, json.dumps(transaction), {'Content-Type': 'application/json'})
                        f = urllib2.urlopen(req)
                        response = f.read()
                        f.close()                        
                        # display a message on the consumer (self)
                        messages.add_message(request, messages.SUCCESS, 'Import succeeded for %s' %(unicode(obj.object),))                                
                    elif transaction['action'] == 'D':
                        if 'ALLOW_DELETE_MODEL_FROM_SERIALIZATION' in dir(settings):
                            if settings.ALLOW_DELETE_MODEL_FROM_SERIALIZATION:
                                if obj.object.__class__.objects.filter(pk=transaction['tx_pk']):
                                    obj_name = unicode(obj.object) 
                                    obj.object.__class__.objects.get(pk=transaction['tx_pk']).delete(transaction_producer=transaction['producer'])
                                    messages.add_message(request, messages.SUCCESS, 'Delete succeeded for %s' %(obj_name,))                                            
                            else:
                                messages.add_message(request, messages.WARNING, 'Delete not allowed. %s' %(obj.object._meta.object_name,))
                                messages.add_message(request, messages.WARNING, 'Delete from imported serialized objects not allowed. See ALLOW_DELETE_MODEL_FROM_SERIALIZATION in settings.')                                                                                            
                        else:
                            msg = 'ALLOW_DELETE_MODEL_FROM_SERIALIZATION global boolean not found in settings.'
                            messages.add_message(request, messages.ERROR, msg)                                                                                            
                    else:
                        raise ValueError, 'Unable to handle imported transaction, unknown \'action\'. Action must be I,U or D. Got %s' % (transaction['action'],)
                    #consumed.append(unicode(obj.object))

                    #except IntegrityError:
                    #    try:
                    #        o = unicode(obj.object)
                    #    except:
                    #        o = obj.object._meta.object_name    
                    #    messages.add_message(request, messages.ERROR, 'Import failed. Integrity Error for %s' %(o,))
                    #except:
                    #    try:
                    #        o = unicode(obj.object)
                    #    except:
                    #        o = obj.object._meta.object_name    
                    #    messages.add_message(request, messages.ERROR, 'Import failed. Unhandled Error for %s' %(o,))    

    
    return render_to_response('new_transactions.html', { 
        'producers': producers,
    },context_instance=RequestContext(request))
