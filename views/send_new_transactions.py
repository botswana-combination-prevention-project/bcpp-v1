import simplejson as json
from django.shortcuts import render_to_response
from django.template import RequestContext
import socket
import urllib2 #import urlopen
from bhp_sync.models import Transaction


def send_new_transactions(request, **kwargs):

    timeout = 5
    url = 'http://localhost:8000/bhp_sync/transaction/?format=json'


    socket_default_timeout = socket.getdefaulttimeout()
    if timeout is not None:
        try:
            socket_timeout = float(timeout)
        except ValueError:
            raise ValueError, "timeout argument of geturl, if provided, must be convertible to a float"
        try:
            socket.setdefaulttimeout(socket_timeout)
        except ValueError:
            raise ValueError, "timeout argument of geturl, if provided, cannot be less than zero"
    """
    try:
        try: 
            # get the json object from the table
            for tx in Transaction.objects.filter(is_sent=False):
                f = urllib2.Request(url, tx, {'Content-Type': 'application/json'})
                response = f.read()
                f.close()
                raise TypeError(response)
        finally: # reset socket timeout
            if timeout is not None:
                socket.setdefaulttimeout(socket_default_timeout) 
    except:
        content = ''        
    """

    for transaction in Transaction.objects.filter(is_sent=False):
        for data in transaction.tx:
            data = json.dumps(data)
            req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
            f = urllib2.urlopen(req)
            response = f.read()
            f.close()
            raise TypeError(response)

    
    raise TypeError()    
    
    return render_to_response('send_new_transactions.html', { 
        'content': content,
    },context_instance=RequestContext(request))
