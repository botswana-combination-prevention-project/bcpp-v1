from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

from edc.device.dispatch.views import dispatch
from edc.device.sync.exceptions import ProducerError

from edc.device.sync.utils import load_producer_db_settings

from ..classes import BcppDispatchController
from ..forms import BcppDispatchForm


@login_required
@csrf_protect
def bcpp_dispatch_view(request, **kwargs):
    """Receives a list of item identifiers, load all producers
    database settings and user selects the producer to dispatch to."""
    try:
        if not load_producer_db_settings():
            raise ProducerError('Error loading producers. None found in model Producer.')
    except ProducerError as producer_error:
        messages.add_message(request, messages.ERROR, str(producer_error))
    return dispatch(request, BcppDispatchController, BcppDispatchForm, app_name='bcpp', **kwargs)
