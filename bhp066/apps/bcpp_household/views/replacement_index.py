import socket

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.conf import settings

from edc.device.sync.helpers import TransactionHelper
from edc.device.sync.models import Producer
from edc.device.sync.exceptions import PendingTransactionError, ProducerError
from edc.device.sync.utils import load_producer_db_settings


def replacement_index(request, **kwargs):
    template = 'replacement_index.html'
    producer_names = []
    message = ''
    try:
        load_producer_db_settings()
        for producer in Producer.objects.filter(is_active=True):
            producer_names.append(producer.name)
            producer_ip = settings.DATABASES[producer.settings_key].get('HOST', None)
            hostname, _, _ = socket.gethostbyaddr(producer_ip)
            TransactionHelper().outgoing_transactions(hostname, producer.name, raise_exception=True)
        if not producer_names:
            messages.add_message(request, messages.WARNING, ('There are no producers in your producer table. Add producers to your producer table'))
    except ProducerError as producer_error:
        messages.add_message(request, messages.ERROR, str(producer_error))
    except TypeError as type_error:
        if 'must be string, not None' in str(type_error):
            messages.add_message(request, messages.ERROR, 'IP for producer {} cannot be None. Set producer.is_active=False to ignore.'.format(producer.name))
        else:
            raise
    except (socket.gaierror, socket.herror):
        messages.add_message(request, messages.ERROR,
                             ('Cannot find producer {} using IP={}. Please confirm both that the '
                              'the IP address in the Producer model and that the '
                              'machine is online and available to the server.'.format(producer.name, producer.producer_ip)))
    except PendingTransactionError:
        messages.add_message(request, messages.ERROR, ('Producer {} has pending transactions'.format(producer.name)))
    return render_to_response(
        template, {
            'message': message,
            'producer_names': producer_names,
            },
        context_instance=RequestContext(request)
    )
