import urllib2
import json
#from sys import platform as _platform
#if _platform == "linux" or _platform == "linux2":
    # linux
#elif _platform == "darwin":
#    import json
from datetime import datetime
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import get_model
from django.contrib import messages
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from bhp_sync.models import Producer, RequestLog, IncomingTransaction, OutgoingTransaction, MiddleManTransaction
from bhp_sync.classes import TransactionProducer


@login_required
def consume_transactions(request, **kwargs):

    if not 'ALLOW_MODEL_SERIALIZATION' in dir(settings):
        messages.add_message(request, messages.ERROR, 'ALLOW_MODEL_SERIALIZATION global boolean not found in settings.')
    producer = None
    middle_man = None
    remote_is_middleman = False
    if 'MIDDLE_MAN' in dir(settings) and settings.MIDDLE_MAN:
        middle_man = True
    else:
        middle_man = False
    if request.user:
        if not 'api_key' in dir(request.user):
            raise ValueError('ApiKey does not exist for user %s. Check if tastypie was added to installed apps or Perhaps run create_api_key().' % (request.user,))
        else:
            if not request.user.api_key:
                raise ValueError('ApiKey not found for user %s. Perhaps run create_api_key().' % (request.user,))
            else:
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
                    if 'MIDDLE_MAN_LIST' in dir(settings):
                        for middle_man_name in settings.MIDDLE_MAN_LIST:
                            if producer.name == middle_man_name:
                                remote_is_middleman = True
                                break
                    else:
                        remote_is_middleman = False
                    # url to producer, add in the producer, username and api_key of the current user
                    data = {'host': producer.url, 'producer': producer.name, 'limit': producer.json_limit, 'username': request.user.username, 'api_key': request.user.api_key.key}
                    if middle_man:
                        #I am a Middleman and pulling from a netbook, so grab eligible(i.e not Synced by Server and any MiddelMan yet) transactions from outgoingtransaction
                        url = '{host}bhp_sync/api_otmr/outgoingtransaction/?format=json&limit={limit}&producer={producer}&username={username}&api_key={api_key}'.format(**data)
                    else:
                        if remote_is_middleman:
                            #I am a Server pulling from a MiddleMan, we dont care who the original producer was, just grab all eligible(i.e not synced by Server yet) tansanctions in MiddleManTransaction table
                            url = '{host}bhp_sync/api_mmtr/middlemantransaction/?format=json&limit={limit}&username={username}&api_key={api_key}'.format(**data)                    
                        else:
                            #I am still a Server, but now pulling from a netbook, just grab all eligible(i.e not synced by Server yet) transactions from OutgoingTransactions table
                            #however pass the producer for filtering on the other side.
                            url = '{host}bhp_sync/api_otsr/outgoingtransaction/?format=json&limit={limit}&producer={producer}&username={username}&api_key={api_key}'.format(**data)
                    request_log = RequestLog()
                    request_log.producer = producer
                    request_log.save()
                    producer.sync_datetime = request_log.request_datetime
                    #producer.sync_status = 'Error'
                    producer.sync_status = '?'
                    producer.save()
                    err = None
                    try:
                        req = urllib2.Request(url=url)
                    except urllib2.URLError, err:
                        producer.sync_status = err
                        producer.save()
                        messages.add_message(request, messages.ERROR, '[A] {0} {1}'.format(err, url))
                    while req:
                        try:
                            f = urllib2.urlopen(req)
                            req = None
                        except urllib2.HTTPError, err:
                            producer.sync_status = err
                            producer.save()
                            messages.add_message(request, messages.ERROR, '[B] {0} {1}'.format(err, url))
                            request_log.status = 'error'
                            request_log.save()
                            req = None
                            if err.code == 404:
                                messages.add_message(request, messages.ERROR, 'Unknown producer. Got %s.' % (kwargs.get('producer')))
                        except urllib2.URLError, err:
                            producer.sync_status = err
                            producer.save()
                            request_log.status = 'error'
                            request_log.save()
                            messages.add_message(request, messages.ERROR, '[C] {0} {1}'.format(err, url))
                            break
                        if not err:
                            # read response from url and decode
                            response = f.read()
                            json_response = None
                            if response:
                                json_response = json.loads(response)
                                # response is limited to 20 objects, if there are more
                                # next will the the url with offset to fetch next 20 (&limit=20&offset=20)
                                if 'meta' in json_response:
                                    if json_response['meta']['next']:
                                        req = urllib2.Request(url=json_response['meta']['next'])
                                    if not json_response['meta']['total_count'] == 0:
                                        messages.add_message(request, messages.INFO, 'Fetching. Limit is %s. Starting at %s of %s' % (json_response['meta']['limit'], json_response['meta']['offset'], json_response['meta']['total_count']))
                                    producer.json_limit = json_response['meta']['limit']
                                    producer.json_total_count = json_response['meta']['total_count']
                                #except:
                                #    messages.add_message(request, messages.ERROR, 'Failed to decode response to JSON from %s URL %s.' % (producer.name,producer.url))
                                if json_response:
                                    messages.add_message(request, messages.INFO, 'Consuming %s new transactions from producer %s URL %s.' % (len(json_response['objects']), producer.name, url))
                                    # 'outgoing_transaction' is the serialized Transaction object from the producer.
                                    # The OutgoingTransaction's object field 'tx' has the serialized
                                    # instance of the data model we are looking for
                                    for outgoing_transaction in json_response['objects']:
                                        # save to IncomingTransaction.
                                        # this will trigger the post_save signal to deserialize tx
                                        #transanction_model = None
                                        if middle_man:
                                            #Read from Netbook's outgoing and create MiddleMan locally.
                                            #transanction_model = MiddleManTransaction
                                            if not MiddleManTransaction.objects.filter(pk=outgoing_transaction['id']).exists():
                                                MiddleManTransaction.objects.create(
                                                    pk=outgoing_transaction['id'],
                                                    tx_name=outgoing_transaction['tx_name'],
                                                    tx_pk=outgoing_transaction['tx_pk'],
                                                    tx=outgoing_transaction['tx'],
                                                    timestamp=outgoing_transaction['timestamp'],
                                                    producer=outgoing_transaction['producer'],
                                                    action=outgoing_transaction['action'])
                                            else:
                                                #transanction already exixts in the MiddleMan. This a highly unlikely outcome
                                                #(NOTE:MiddleMan only consumes from netbook.)but if it occurs then mark it as 
                                                #not consumed by the Server
                                                middle_man_transaction = MiddleManTransaction.objects.get(pk=outgoing_transaction['id'])
                                                middle_man_transaction.is_consumed_server = False
                                                middle_man_transaction.is_error = False
                                                middle_man_transaction.save()
                                        else:
                                            #Then i must be a SERVER
                                            if not IncomingTransaction.objects.filter(pk=outgoing_transaction['id']).exists():
                                                IncomingTransaction.objects.create(
                                                    pk=outgoing_transaction['id'],
                                                    tx_name=outgoing_transaction['tx_name'],
                                                    tx_pk=outgoing_transaction['tx_pk'],
                                                    tx=outgoing_transaction['tx'],
                                                    timestamp=outgoing_transaction['timestamp'],
                                                    producer=outgoing_transaction['producer'],
                                                    action=outgoing_transaction['action'])
                                            else:
                                                #START HERE
                                                #a little tricky cause it could be from Middleman or Netbook, depending on which was synced first
                                                #but either way, what we want to do is ignore the tranction that already exists in the server,
                                                #irregardles of where it comes from, it should exactly be the same transanction.
                                                
                                                #incoming_transaction = IncomingTransaction.objects.get(pk=outgoing_transaction['id'])
                                                #incoming_transaction.is_consumed = False
                                                #incoming_transaction.is_error = False
                                                #incoming_transaction.save()
                                                pass
                                        # POST success back to to the producer
                                        if middle_man:
                                            outgoing_transaction['is_consumed_middleman'] = True
                                            outgoing_transaction['is_consumed_server'] = False
                                        else:
                                            if not outgoing_transaction['is_consumed_middleman']:
                                                #transanction was consumed straight in the Server, MiddleMan bypassed
                                                outgoing_transaction['is_consumed_middleman'] = False
                                            outgoing_transaction['is_consumed_server'] = True
                                        outgoing_transaction['consumer'] = str(TransactionProducer())
                                        req = urllib2.Request(url, json.dumps(outgoing_transaction, cls=DjangoJSONEncoder), {'Content-Type': 'application/json'})
                                        f = urllib2.urlopen(req)
                                        response = f.read()
                                        f.close()
                                        producer.sync_status = 'OK'
                                        producer.sync_datetime = datetime.today()

                    # removed: syncing should no longer change the dispatch status
#                    if 'ALLOW_DISPATCH' in dir(settings) and settings.ALLOW_DISPATCH:
#                        DispatchItem = get_model('bhp_dispatch', 'DispatchItem')
#                        if OutgoingTransaction.objects.using(producer.name).filter(is_consumed=False).exists():
#                            messages.add_message(request, messages.ERROR, 'Not all Transactions consumed from producer %s.' % (kwargs.get('producer')))
#                        else:
#                            for item in DispatchItem.objects.filter(producer__name=producer.name, is_dispatched=True):
#                                item.is_dispatched = False
#                                item.return_datetime = datetime.today()
#                                item.save()

                    producer.save()
        return redirect('/bhp_sync/consumed/{0}/'.format(producer.name))
