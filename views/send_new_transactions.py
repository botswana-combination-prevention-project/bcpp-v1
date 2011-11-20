import urllib2, base64, socket
import simplejson as json
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


def send_new_transactions(request, **kwargs):

    if not 'ALLOW_MODEL_SERIALIZATION' in dir(settings):
        messages.add_message(request, messages.ERROR, 'ALLOW_MODEL_SERIALIZATION global boolean not found in settings.')                                                                                            
    
    if not request.user.api_key:
        raise ValueError, 'ApiKey not found for user %s. Perhaps run create_api_key().' % (request.user,)
                
    timeout = 5
    socket_default_timeout = socket.getdefaulttimeout()        
    #if timeout is not None:
    #    try:
    #        socket_timeout = float(timeout)
    #    except ValueError:
    #        raise ValueError, "timeout argument of geturl, if provided, must be convertible to a float"
    #    try:
    #        socket.setdefaulttimeout(socket_timeout)
    #    except ValueError:
    #        raise ValueError, "timeout argument of geturl, if provided, cannot be less than zero"

    consumed = []
    
    if kwargs.get('producer'):
        producers = Producer.objects.filter(name__iexact=kwargs.get('producer'))
        if not producers:
            messages.add_message(request, messages.ERROR, 'Unknown producer. Got %s.' % (kwargs.get('producer')))          
    else:
        producers = Producer.objects.all()

    for producer in producers:
        url = '%s?producer=%s&username=%s&api_key=%s' % (producer.url, producer.name, request.user.username, request.user.api_key.key)
        request_log = RequestLog()
        request_log.producer = producer
        request_log.save()
        
        f = urllib2.urlopen(url)
        response = f.read()
        json_response = None
        try:
            json_response =  json.loads(response)   
        except:   
            messages.add_message(request, messages.ERROR, 'Failed to decode response to JSON from %s URL %s.' % (producer.name,producer.url))  

        if json_response:
            error_list = []
            messages.add_message(request, messages.INFO, 'Fetching %s transactions from producer %s URL %s.' % (len(json_response['objects']), producer.name,url))                                                                                                    
            for data in json_response['objects']:
                for obj in serializers.deserialize("json",data['tx']):
                    #try:
                    if data['action'] == 'I' or data['tx'] == 'U':
                        obj.save()
                        obj.object.save(transaction_producer=data['producer'])
                        messages.add_message(request, messages.SUCCESS, 'Import succeeded for %s' %(unicode(obj.object),))                                
                    elif data['action'] == 'D':
                        if 'ALLOW_DELETE_MODEL_FROM_SERIALIZATION' in dir(settings):
                            if settings.ALLOW_DELETE_MODEL_FROM_SERIALIZATION:
                                if obj.object.__class__.objects.filter(pk=data['tx_pk']):
                                    obj.object.__class__.objects.get(pk=data['tx_pk']).delete(transaction_producer=data['producer'])
                                    messages.add_message(request, messages.SUCCESS, 'Delete succeeded for %s' %(unicode(obj.object),))                                            
                            else:
                                messages.add_message(request, messages.WARNING, 'Delete from imported serialized objects not allowed. See ALLOW_DELETE_MODEL_FROM_SERIALIZATION in settings.')                                                                                            
                        else:
                            msg = 'ALLOW_DELETE_MODEL_FROM_SERIALIZATION global boolean not found in settings.'
                            messages.add_message(request, messages.ERROR, msg)                                                                                            
                    else:
                        raise ValueError, 'Unable to handle imported transaction, unknown \'action\'. Action must be I,U or D. Got %s' % (data['action'],)
                    #consumed.append(unicode(obj.object))

                    #except IntegrityError:
                    #    try:
                    #        o = unicode(obj.object)
                    #    except:
                    #        o = obj.object._meta.object_name    
                    #    messages.add_message(request, messages.ERROR, 'Import failed. Integrity Error for %s' %(o,))
                    #except:
                    #    messages.add_message(request, messages.ERROR, 'Import failed. Unhandled Error for %s' %(obj,))    

            #for transaction in Transaction.objects.filter(is_sent=False):
            #    for data in transaction.tx:
            #        data = json.dumps(data)
            #        req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
            #        req.add_header("Authorization", "Basic %s" % base64string)
            #        f = urllib2.urlopen(req)
            #        response = f.read()
            #        f.close()
            #        raise TypeError(response)

    
    return render_to_response('send_new_transactions.html', { 
        'producers': producers,
    },context_instance=RequestContext(request))
