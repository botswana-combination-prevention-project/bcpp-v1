import socket
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from edc.device.sync.models import Producer
from edc.device.device.classes import Device


@login_required
def bcpp_sync(request, **kwargs):

    selected_producer = kwargs.get('selected_producer', None)
    producers = Producer.objects.filter(is_active=True)
    is_server = Device().is_server
    is_middleman = Device().is_middleman
    return render_to_response('bcpp_sync.html', {
        'is_server': is_server,
        'is_middleman': is_middleman,
        'producers': producers,
        'hostname': socket.gethostname(),
        'selected_producer': selected_producer
    }, context_instance=RequestContext(request))
