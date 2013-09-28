from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from edc_lib.bhp_dispatch.views import dispatch
from bcpp_dispatch.classes import BcppDispatchController
from bcpp_dispatch.forms import BcppDispatchForm


@login_required
@csrf_protect
def bcpp_dispatch(request, **kwargs):
    """Receives a list of item identifiers and user selects the producer to dispatch to."""
    return dispatch(request, BcppDispatchController, BcppDispatchForm, **kwargs)
