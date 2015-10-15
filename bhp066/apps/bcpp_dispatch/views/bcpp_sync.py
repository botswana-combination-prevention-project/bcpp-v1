import socket

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from edc_device import device
from edc.device.sync.models import Producer, OutgoingTransaction


@login_required
def bcpp_sync(request, **kwargs):

    selected_producer = kwargs.get('selected_producer', None)
    producers = Producer.objects.filter(is_active=True)
    return render_to_response('bcpp_sync.html', {
        'is_server': device.is_server,
        'is_middleman': device.is_middleman,
        'producers': producers,
        'hostname': socket.gethostname(),
        'selected_producer': selected_producer,
        'producer_cls': Producer,
        'outgoingtransaction_cls': OutgoingTransaction,
        'app_name': settings.APP_NAME,
    }, context_instance=RequestContext(request))
