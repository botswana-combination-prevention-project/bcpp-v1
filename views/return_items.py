from django.contrib.auth.decorators import login_required
#from django.contrib import messages
#from django.core.exceptions import ObjectDoesNotExist
#from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from bhp_sync.models import Producer
from bhp_dispatch.classes import ReturnController


@login_required
def return_items(request, **kwargs):
    """ Return items from the producer to the source."""
    producer = Producer.objects.get(name__iexact=kwargs.get('producer', None))
    if producer:
        ReturnController('default', producer.name).return_dispatched_items()
    return render_to_response(
        'checkin_households.html', {'producer': producer, },
        context_instance=RequestContext(request)
        )
