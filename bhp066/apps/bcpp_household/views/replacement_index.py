import socket

from collections import namedtuple

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db import OperationalError

from edc.device.sync.helpers import TransactionHelper
from edc.device.sync.models import Producer
from edc.device.sync.exceptions import PendingTransactionError, ProducerError
from edc.device.sync.utils import load_producer_db_settings, getproducerbyaddr

from ..exceptions import ReplacementError
from ..models import Replaceable

ProducerStatus = namedtuple('ProducerStatus', 'producer_name settings_key ip online synced error replaceables_count replaceables_last_updated')


@login_required
def replacement_index(request, **kwargs):
    template = 'replacement_index.html'
    producers = []
    load_producer_db_settings()
    for producer in Producer.objects.filter(is_active=True):
        try:
            error = False
            hostname = None
            outgoing_transactions = None
            hostname, _, _ = getproducerbyaddr(producer)  # is producer online?
            outgoing_transactions = TransactionHelper().outgoing_transactions(hostname, producer.name, raise_exception=True)
        except ProducerError as producer_error:
            error = True
            messages.add_message(request, messages.ERROR, str(producer_error))
        except TypeError as type_error:
            error = True
            if 'must be string, not None' in str(type_error):
                messages.add_message(request, messages.ERROR, (
                    'IP for producer {} cannot be None. Set producer.is_active=False '
                    'to ignore.').format(producer.name))
            else:
                raise
        except (socket.gaierror, socket.herror):
            error = True
            messages.add_message(request, messages.ERROR, (
                'Cannot find producer {} using IP={}. Please confirm both that the '
                'the IP address in the Producer model and that the '
                'machine is online and available to the server.'.format(producer.name, producer.producer_ip)))
        except OperationalError as operational_error:
            raise ReplacementError('Unable to connect to producer with settings key \'{}\'. '
                                   'Got {}'.format(producer.settings_key, str(operational_error)))
        except PendingTransactionError:
            error = True
            messages.add_message(request, messages.ERROR, (
                'Producer {} has pending transactions'.format(producer.name)))
        finally:
            replaceables_count = Replaceable.objects.filter(
                producer_name=producer.name,
                replaced=False).count()
            replaceables_last_updated = Replaceable.objects.filter(
                producer_name=producer.name,
                replaced=False).aggregate(Max('created'))
            producers.append(ProducerStatus(
                producer_name=producer.name,
                settings_key=producer.settings_key,
                ip=producer.producer_ip,
                online=True if hostname else False,
                synced=True if not outgoing_transactions else False,
                error=error,
                replaceables_count=replaceables_count,
                replaceables_last_updated=replaceables_last_updated.get('created__max'))
                )

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
