import socket
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from bhp_sync.models import Producer


@login_required
def index(request, **kwargs):
    selected_producer = kwargs.get('selected_producer', None)
    producers = Producer.objects.filter(is_active=True)
    return render_to_response('sync.html', {
        'producers': producers,
        'hostname': socket.gethostname(),
        'selected_producer': selected_producer
    }, context_instance=RequestContext(request))
