from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages

from edc.device.sync.exceptions import PendingTransactionError, ProducerError
from edc.device.sync.utils import load_producer_db_settings

from ..helpers import ReplacementHelper


def check_replacements(request):
    """Get all plots to be replaced.

    Filter plots to be replaced by calling replacement methods that return replacement household.
    """
    template = 'check_replacements.html'
    replaceables = []
    try:
        producer_name = request.POST.get('producer_name')
        load_producer_db_settings(producer_name)
        if producer_name:
            replacement_helper = ReplacementHelper()
            replaceables = replacement_helper.replaceable_households(producer_name) + replacement_helper.replaceable_plots(producer_name)
        if not replaceables:
            messages.add_message(request, messages.INFO, "There are no replaceable households or plots from {}".format(str(producer_name)))
    except ProducerError as producer_error:
        messages.add_message(request, messages.ERROR, str(producer_error))
    except PendingTransactionError as pending_transaction_error:
        messages.add_message(request, messages.ERROR, str(pending_transaction_error))
    return render_to_response(
        template, {
            'replaceables': replaceables,
            'replacement_count': len(replaceables),
            'producer_name': producer_name,
            },
        context_instance=RequestContext(request)
        )
