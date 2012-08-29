import socket
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from bhp_sync.models import Producer


@login_required
def index(request, **kwargs):

    producers = Producer.objects.filter(is_active=True)
    return render_to_response('sync.html', {
        'producers': producers,
        'hostname': socket.gethostname(),
    }, context_instance=RequestContext(request))
