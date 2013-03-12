import socket
import logging
from datetime import datetime
from django.conf import settings
from django.db.models.query import QuerySet
from django.db.models import signals
from django.core import serializers
from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_model, Q, Count, Max
from django.db import IntegrityError
from bhp_sync.models import BaseSyncUuidModel
from bhp_sync.models.signals import serialize_on_save
from bhp_sync.helpers import TransactionHelper
from bhp_dispatch.exceptions import DispatchError, DispatchModelError
from bhp_sync.exceptions import PendingTransactionError

logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class Base(object):

    APP_NAME = 0
    MODEL_NAME = 1

    def __init__(self, using_source, using_destination, **kwargs):
        """Initializes and verifies arguments ``using_source`` and ``using_destination``.

        Args:
            ``using_source``: settings.DATABASE key for source. Source is the server so must
                          be 'default' if running on the server and 'server'
                          if running on the device.
            ``using_destination``: settings.DATABASE key for destination. If running from the server
                               this key must exist in settings.DATABASES. If on the device, must be 'default'.
                               In either case, ``using_destination`` must be found in the
                               source :class:`Producer` model as producer.settings_key (see :func:`set_producer`.)

        Keywords:
            ``server_device_id``: settings.DEVICE_ID for server (default='99')

        Settings:
            DISPATCH_APP_LABELS = a list of app_labels for apps that contain models to be monitored by bhp_dispatch. Models in apps not
                                  here will be ignored by default. To ignore a model that exists in an app listed here, override the
                                  :func:`ignore_for_dispatch` method on the model. See model base class :class:`BaseSyncUuidModel` in
                                  module :mod:`bhp_sync`. For example: DISPATCH_APP_LABELS = ['mochudi_household', 'mochudi_subject', 'mochudi_lab']
            """
        self._using_source = None
        self._using_destination = None
        self._producer = None
        self.server_device_id = kwargs.get('server_device_id', '99')
        self.exception = kwargs.get('exception', DispatchError)
        self.preparing_status = kwargs.get('preparing_netbook',None)
        if not 'DISPATCH_APP_LABELS' in dir(settings):
            raise ImproperlyConfigured('Attribute DISPATCH_APP_LABELS not found. Add to settings. e.g. DISPATCH_APP_LABELS = [\'mochudi_household\', \'mochudi_subject\', \'mochudi_lab\']')
        #if not 'ALLOW_DISPATCH' in dir(settings):
        #    raise self.exception('Settings attribute \'ALLOW_DISPATCH\' not found (ALLOW_DISPATCH=<TRUE/FALSE>). Please add to your settings.py.')
        #if not 'DISPATCH_MODEL' in dir(settings):
        #    raise self.exception('Settings attribute \'DISPATCH_MODEL\' not found where DISPATCH_MODEL=(app_label, model_name). Please add to your settings.py.')
        if using_source == using_destination:
            raise self.exception('Arguments \'<source>\' and \'<destination\'> cannot be the same. Got \'{0}\' and \'{1}\''.format(using_source, using_destination))
        self.set_using_source(using_source)
        self.set_using_destination(using_destination)
        self.set_producer()
        return None

    def set_using_source(self, using_source=None):
        """Sets the ORM `using` parameter for data access on the "source"."""
        if not using_source:
            raise self.exception('Parameters \'using_source\' cannot be None')
        if using_source not in ['server', 'default']:
            raise self.exception('Argument \'<using_source\'> must be either \'default\' (if run from server) or \'server\' if not run from server.')
        if settings.DEVICE_ID == self.server_device_id and using_source != 'default':
            raise self.exception('Argument \'<using_source\'> must be \'default\' if running on the server (check settings.DEVICE).')
        if settings.DEVICE_ID != self.server_device_id and using_source == 'default':
            raise self.exception('Argument \'<using_source\'> must be \'server\' if running a device (check settings.DEVICE).')
        if self.is_valid_using(using_source, 'source'):
            self._using_source = using_source

    def get_using_source(self):
        """Gets the ORM `using` parameter for "source"."""
        if not self._using_source:
            self.set_using_source()
        return self._using_source

    def set_using_destination(self, using_destination=None):
        """Sets the ORM `using` parameter for data access on the "destination"."""
        if not using_destination:
            raise self.exception('Parameters \'using_destination\' cannot be None')
        if using_destination == 'server':
            raise self.exception('Argument \'<using_destination\'> cannot be \'server\'.')
        if settings.DEVICE_ID == self.server_device_id and using_destination == 'default':
            raise self.exception('Argument \'<using_destination\'> cannot be \'default\' if running on the server (check settings.DEVICE).')
        if self.is_valid_using(using_destination, 'destination'):
            self._using_destination = using_destination
#        if self.get_using_source() == 'default':
#            # when source is default (running on server), destination must be an active producer settings key
#            if not using_destination in Producer.objects.using(self.get_using_source()).filter(is_active=True).values_list('settings_key'):
#                raise self.exception("Destination {0} does not match any database settings keys of the active producers".format(using_destination))

    def get_using_destination(self):
        """Gets the ORM `using` parameter for "destination"."""
        if not self._using_destination:
            self.set_using_destination()
        return self._using_destination

    def is_valid_using(self, using, label):
        """Confirms an ORM `using` parameter is valid by checking :file:`settings.py`."""
        if not [dbkey for dbkey in settings.DATABASES.iteritems() if dbkey[0] == using]:
            raise ImproperlyConfigured('Cannot find {1} key \'{0}\' in settings attribute DATABASES. Please add to settings.py.'.format(using, label))
        return True

    def set_producer(self):
        """Sets the instance of the current producer based on the ORM `using` parameter for the destination
        and refreshes the list of dispatched Dispatch models.

        .. note:: The producer must always exist on the source. If dispatching via the device, try to
                  find a producer with the settings_key of the format ``DEVICE_HOSTNAME-DBNAME``
                  where DBNAME is the NAME attribute of the ``default`` DATABASE on the device."""
        Producer = get_model('bhp_sync', 'Producer')
        settings_key = None
        # try to determine producer from using_destination
        if self.get_using_destination() == 'default':
            # try to find the producer on the server with hostname + database name
            settings_key = '{0}-{1}'.format(socket.gethostname().lower(), settings.DATABASES.get('default').get('NAME'))
            if Producer.objects.using(self.get_using_source()).filter(settings_key=settings_key, is_active=True).exists():
                self._producer = Producer.objects.using(self.get_using_source()).get(settings_key=settings_key, is_active=True)
        else:
            if Producer.objects.using(self.get_using_source()).filter(settings_key=self.get_using_destination(), is_active=True).exists():
                self._producer = Producer.objects.using(self.get_using_source()).get(settings_key=self.get_using_destination(), is_active=True)
        if not self._producer:
            raise DispatchError('Dispatcher cannot find producer {2} with settings key {0} '
                            'on the source {1}.'.format(self.get_using_destination(), self.get_using_source(), settings_key))
        # check the producers DATABASES key exists
        # TODO: what if producer is "me", e.g settings key is 'default'
        if not self.get_using_destination() == 'default':
            settings_key = self._producer.settings_key
            if not [dbkey for dbkey in settings.DATABASES.iteritems() if dbkey[0] == settings_key]:
                raise ImproperlyConfigured('Dispatcher expects settings attribute DATABASES to have a NAME '
                                           'key to the \'producer\'. Got name=\'{0}\', settings_key=\'{1}\'.'.format(self._producer.name, self._producer.settings_key))

    def get_producer(self):
        """Returns an instance of the current producer."""
        if not self._producer:
            self.set_producer()
        return self._producer

    def get_producer_name(self):
        return self.get_producer().name

    def has_pending_transactions(self, models):
        return self.has_incoming_transactions(models) or self.has_outgoing_transactions()

    def has_outgoing_transactions(self):
        """Check if destination has pending Outgoing Transactions by checking is_consumed in
           bhp_sync.outgoing_transactions.
        """
        return TransactionHelper().has_outgoing(self.get_using_destination())

    def has_incoming_transactions(self, models=None):
        """Check if source has pending Incoming Transactions for this producer and model(s).
        """
        retval = False
        if TransactionHelper().has_incoming_for_producer(self.get_producer_name(), self.get_using_source()):
            retval = True
        if not retval:
            if models:
                if isinstance(models, QuerySet):
                    models = [model for model in models]
                if not isinstance(models, list):
                    models = [models]
                if TransactionHelper().has_incoming_for_model([model._meta.object_name for model in models], self.get_using_source()):
                    retval = True
        return retval

#    def update_model(self, model, **kwargs):
#        self.dispatch_model_as_json(model, **kwargs)

    def get_recent(self, model_cls, destination_hostname=None):
        """Returns a queryset of the most recent instances from the model for all but the current host."""
        instances = model_cls.objects.none()
        if not destination_hostname:
            destination_hostname = socket.gethostname()
        options = self.get_last_modified_options(model_cls)
        if options:
            qset = Q()
            for dct in options:
                qset.add(Q(**dct), Q.OR)
            source_instances = model_cls.objects.using(self.get_using_source()).filter(qset).order_by('id')
        else:
            source_instances = model_cls.objects.using(self.get_using_source()).all().order_by('id')
        return source_instances

    def get_last_modified_options(self, model_cls):
        """Returns a dictionary of {'hostname_modified': '<hostname>', 'modified__max': <date>, ... }."""
        options = []
        # get hostnames from source and populate default dictionary
        if 'hostname_modified' in [field.name for field in model_cls._meta.fields]:
            hostnames = model_cls.objects.using(self.get_using_source()).values('hostname_modified').annotate(Count('hostname_modified')).order_by()
            for item in hostnames:
                options.append({'hostname_modified': item.get('hostname_modified'), 'modified__gt': datetime(1900, 1, 1)})
            valuesset = model_cls.objects.using(self.get_using_destination()).values('hostname_modified').all().annotate(Max('modified')).order_by()
            for item in valuesset:
                for n, dct in enumerate(options):
                    if dct.get('hostname_modified') == item.get('hostname_modified'):
                        dct.update({'hostname_modified': item.get('hostname_modified'), 'modified__gt': item.get('modified__max')})
                        options[n] = dct
        return options

    def model_to_json(self, model_cls):
        self._to_json([instance for instance in model_cls.objects.all()])

    def _to_json(self, model_instances):
        """Serialize models on source and deserialize on destination.

        ..warning:: This method assumes you have confirmed that the model_instances are "already dispatched" or not.

        """
        base_model_class = BaseSyncUuidModel
        # check for pending transactions
        if self.has_outgoing_transactions():
            raise PendingTransactionError('Producer \'{0}\' has pending outgoing transactions. Run bhp_sync first.'.format(self.get_producer_name()))
        if self.has_incoming_transactions(model_instances):
            raise PendingTransactionError('Producer \'{0}\' has pending incoming transactions on this server. Consume them first.'.format(self.get_producer_name()))
        if model_instances:
            # convert to list if not iterable
            if not isinstance(model_instances, (list, QuerySet)):
                model_instances = [model_instances]
            # confirm all model_instances are of the correct base class
            for instance in model_instances:
                if not isinstance(instance, base_model_class):
                    raise DispatchModelError('For dispatch, user model {0} must be an instance of \'{1}\'.'.format(instance, base_model_class))
            #serialize
            json = serializers.serialize('json', model_instances, use_natural_keys=True)
            # deserialize on destination
            for d_obj in serializers.deserialize("json", json, use_natural_keys=True):
                #if d_obj.object.is_dispatched_as_item():
                #    raise AlreadyDispatchedItem('Model {0}-{1} is currently dispatched'.format(d_obj.object._meta.object_name, d_obj.object.pk))
                try:
                    # disconnect signal to avoid creating transactions on the source for data saved on destination
                    signals.post_save.disconnect(serialize_on_save, weak=False, dispatch_uid="serialize_on_save")
                    #save
                    d_obj.save(using=self.get_using_destination())
                    # reconnect
                    signals.post_save.connect(serialize_on_save, weak=False, dispatch_uid="serialize_on_save")
                except IntegrityError as e:
                    logger.info(e)
                    logger.info(e.message)
                    if 'is not unique' in e.message:
                        raise DispatchError('Model instance {0} is already on producer {1}.'.format(d_obj.object, self.get_producer_name()))
                    if 'Duplicate' in e.message:
                        pass
                    elif 'Cannot add or update a child row' in e.message:
                        # assume Integrity error was because of missing ForeignKey data
                        self.dispatch_foreign_key_instances(self.get_dispatch_item_app_label())
                        # try again
                        # disconnect signal
                        signals.post_save.disconnect(serialize_on_save, weak=False, dispatch_uid="serialize_on_save")
                        #save
                        d_obj.save(using=self.get_using_destination())
                        # reconnect
                        signals.post_save.connect(serialize_on_save, weak=False, dispatch_uid="serialize_on_save")
                    else:
                        raise
                except:
                    raise
