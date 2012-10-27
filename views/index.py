import socket
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from bhp_sync.models import Producer


@login_required
def index(request, **kwargs):
    show_checkin_link = False
    if settings.ALLOW_MODEL_CHECKOUT:
        show_checkin_link = True
    producers = Producer.objects.filter(is_active=True)
    return render_to_response('sync.html', {
        'producers': producers,
        'hostname': socket.gethostname(),
        'show_checkin_link': show_checkin_link,
        'CHECKOUT_APP': settings.CHECKOUT_APP
    }, context_instance=RequestContext(request))
