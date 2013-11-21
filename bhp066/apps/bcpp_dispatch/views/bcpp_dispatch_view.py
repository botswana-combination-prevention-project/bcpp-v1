from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from edc.device.dispatch.views import dispatch
from apps.bcpp_dispatch.classes import BcppDispatchController
from apps.bcpp_dispatch.forms import BcppDispatchForm


@login_required
@csrf_protect
def bcpp_dispatch_view(request, **kwargs):
    """Receives a list of item identifiers and user selects the producer to dispatch to."""
    return dispatch(request, BcppDispatchController, BcppDispatchForm, app_name='bcpp', **kwargs)
