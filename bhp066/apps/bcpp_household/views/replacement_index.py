from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from edc.device.sync.models import Producer
from edc.device.sync.utils import load_producer_db_settings

from ..models import Replaceable
from ..utils import get_producer_status


@login_required
def replacement_index(request, **kwargs):
    template = 'replacement_index.html'
    producers = []
    load_producer_db_settings()
    for producer in Producer.objects.filter(is_active=True):
        producer_status = get_producer_status(producer)
        if producer_status.error_message:
            messages.add_message(request, messages.ERROR, producer_status.error_message)
        producers.append(producer_status)
    if not producers:
        messages.add_message(request, messages.WARNING, (
            'There are no producers in your producer table. Add producers '
            'to your producer table'))
    return render_to_response(
        template, {
            'producers': producers,
            'producer': Producer,
            'replaceable': Replaceable,
        },
        context_instance=RequestContext(request)
    )
