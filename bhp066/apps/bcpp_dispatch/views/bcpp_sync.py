import socket

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from edc.device.device.classes import Device
from edc.device.sync.models import Producer, OutgoingTransaction


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
        'selected_producer': selected_producer,
        'producer_cls': Producer,
        'outgoingtransaction_cls': OutgoingTransaction,
        'app_name': settings.APP_NAME,
    }, context_instance=RequestContext(request))
