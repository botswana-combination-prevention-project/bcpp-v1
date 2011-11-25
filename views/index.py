from django.shortcuts import render_to_response
from django.template import RequestContext
from bhp_sync.models import Producer


def index(request, **kwargs):


    producers = Producer.objects.filter(is_active=True)
    
    
    return render_to_response('sync.html', { 
        'producers': producers,
    },context_instance=RequestContext(request))    
