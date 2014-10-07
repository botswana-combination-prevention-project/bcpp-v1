import socket
from collections import namedtuple

from django.db.utils import ConnectionDoesNotExist
from django.db import OperationalError
from django.db.models import Max

from edc.device.sync.helpers import TransactionHelper
from edc.device.sync.exceptions import PendingTransactionError, ProducerError
from edc.device.sync.utils import getproducerbyaddr

from ..models import Replaceable

ProducerStatus = namedtuple('ProducerStatus', (
    'producer_name settings_key ip online synced error replaceables_count '
    'replaceables_last_updated error_message'))


def get_producer_status(producer=None, check_online=True):
    error_message = None
    outgoing_transactions = None
    hostname = None
    try:
        if check_online:
            hostname, _, _ = getproducerbyaddr(producer)
            outgoing_transactions = TransactionHelper().outgoing_transactions(
                hostname, producer.name, raise_exception=True)
        else:
            hostname = '?'
            outgoing_transactions = '?'
    except ProducerError as producer_error:
        error_message = str(producer_error)
    except TypeError as type_error:
        if 'must be string, not None' in str(type_error):
            error_message = (
                'IP for producer {} cannot be None. Set producer.is_active=False '
                'to ignore.').format(producer.name)
        else:
            raise
    except (socket.gaierror, socket.herror):
        error_message = (
            'Cannot find producer {} using IP={}. Please confirm both that the '
            'the IP address in the Producer model and that the '
            'machine is online and available to the server.'.format(producer.name, producer.producer_ip))
    except ConnectionDoesNotExist as connection_does_not_exist:
        error_message = str(connection_does_not_exist)
    except OperationalError as operational_error:
        error_message = (
            'Unable to connect to producer with settings key \'{}\'. '
            'Got {}').format(producer.settings_key, str(operational_error))
    except PendingTransactionError:
        error_message = ('Producer {} has pending transactions'.format(producer.name))
    finally:
        replaceables_count = Replaceable.objects.filter(
            producer_name=producer.name,
            replaced=False).count()
        replaceables_last_updated = Replaceable.objects.filter(
            producer_name=producer.name,
            replaced=False).aggregate(Max('created'))
        producer_status = ProducerStatus(
            producer_name=producer.name,
            settings_key=producer.settings_key,
            ip=producer.producer_ip,
            online=True if hostname else False,
            synced=True if not outgoing_transactions else False,
            error=True if error_message else False,
            replaceables_count=replaceables_count,
            replaceables_last_updated=replaceables_last_updated.get('created__max'),
            error_message=error_message)
    return producer_status
