from django.contrib import messages
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from edc.device.sync.exceptions import ProducerError
from edc.device.sync.utils import load_producer_db_settings


@login_required
def load_producer_databases(request, **kwargs):
    """Add all producer database settings to the setting's file 'DATABASE' attribute."""
    template = 'load_producer_databases.html'
    try:
        load_producer_db_settings()
        messages.add_message(request, messages.SUCCESS, (
            'Producers have been loaded from model Producer into settings.'))
    except ProducerError as producer_error:
        messages.add_message(request, messages.ERROR, str(producer_error))
    return render_to_response(
        template, {},
        context_instance=RequestContext(request))
