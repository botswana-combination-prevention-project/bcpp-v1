from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.db import OperationalError
from django.contrib.auth.decorators import login_required

from edc.device.sync.models import Producer
from edc.device.sync.exceptions import PendingTransactionError, ProducerError
from edc.device.sync.utils import load_producer_db_settings, getproducerbyaddr

from ..helpers import ReplacementHelper


@login_required
def check_replacements(request):
    """Get all plots to be replaced.

    Filter plots to be replaced by calling replacement methods that
    return replacement household.
    """
    template = 'check_replacements.html'
    replaceables = []
    try:
        producer_name = request.POST.get('producer_name')
        load_producer_db_settings(producer_name)
        if producer_name:
            producer = Producer.objects.get(name=producer_name)
            getproducerbyaddr(producer)  # is producer available in DNS/Hosts file?
            replacement_helper = ReplacementHelper()
            replaceables = list(replacement_helper.replaceable_plots(producer.settings_key))
            replaceables.extend(list(replacement_helper.replaceable_households(producer.settings_key)))
        if not replaceables:
            messages.add_message(request, messages.INFO, (
                "There are no replaceable plots or households that are dispatched to "
                "producer \'{}\'").format(str(producer.name)))
    except Producer.DoesNotExist:
        messages.add_message(request, messages.ERROR, (
            '\'{}\' not a valid producer. See model Producer.').format(producer_name))
    except ProducerError as producer_error:
        messages.add_message(request, messages.ERROR, str(producer_error))
    except PendingTransactionError as pending_transaction_error:
        messages.add_message(request, messages.ERROR, str(pending_transaction_error))
    except OperationalError as operational_error:
        messages.add_message(request, messages.ERROR, ('Unable to connect to producer {} with current settings. '
                                                       'Got {}').format(producer_name, str(operational_error)))
    return render_to_response(
        template, {
            'replaceables': replaceables,
            'replacement_count': len(replaceables),
            'producer_name': producer_name,
            'producer': Producer,
        },
        context_instance=RequestContext(request)
    )
