import socket
import logging
from datetime import datetime
from django.conf import settings
from django.core.serializers.base import DeserializationError
from django.db import IntegrityError
from django.db.models.query import QuerySet
from django.db.models import signals, get_model
from django.db.models import ForeignKey, OneToOneField
from django.core import serializers
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q, Count, Max
from lab_base_model.models import BaseLabListModel, BaseLabListUuidModel
from bhp_base_model.models import BaseListModel
from bhp_visit.models import VisitDefinition
from bhp_variables.models import StudySite
from bhp_lab_tracker.models import BaseHistoryModel
from bhp_entry.models import BaseEntryBucket
from bhp_visit_tracking.models.signals import base_visit_tracking_add_or_update_entry_buckets_on_post_save, base_visit_tracking_on_post_save
from bhp_sync.classes import BaseProducer
from bhp_sync.models.signals import serialize_on_save
from bhp_lab_tracker.models.signals import tracker_on_post_save
from bhp_sync.helpers import TransactionHelper
#from bhp_lab_tracker.models import HistoryModel
from bhp_dispatch.exceptions import ControllerBaseModelError
from bhp_sync.exceptions import PendingTransactionError
from controller_register import registered_controllers


logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class BaseController(BaseProducer):

    APP_NAME = 0
    MODEL_NAME = 1

    def __repr__(self):
        return self._repr()

    __str__ = __repr__

    def __del__(self):
        """Deregisters for this producer.settings_key."""
        registered_controllers.deregister(self)

    def _repr(self):
        return '{0}for {1}'.format('BaseController', self.get_producer().settings_key)

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
        super(BaseController, self).__init__(using_source, using_destination, **kwargs)
        self.fk_instances = []
        self.preparing_status = kwargs.get('preparing_netbook', None)
        if not 'DISPATCH_APP_LABELS' in dir(settings):
            raise ImproperlyConfigured('Attribute DISPATCH_APP_LABELS not found. Add to settings. e.g. DISPATCH_APP_LABELS = [\'mochudi_household\', \'mochudi_subject\', \'mochudi_lab\']')
        self.set_producer()
        self._session_container = {}
        return None

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

    def get_recent(self, model_cls, destination_hostname=None):
        """Returns a queryset of the most recent instances from the model for all but the current host."""
        source_instances = model_cls.objects.none()
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

    def model_to_json(self, model_cls, additional_base_model_class=None):
        """Sends all instances of the model class to :func:`_to_json`."""
        self._to_json(model_cls.objects.all(), additional_base_model_class)

    def is_allowed_base_model_cls(self, cls, additional_base_model_class=None):
        """Returns True or raises an exception if the class is a subclass of a base model class allowed for serialization."""
        if not issubclass(cls, self._get_allowed_base_models(additional_base_model_class)):
            raise ControllerBaseModelError('For dispatch, user model \'{0}\' must be a subclass of \'{1}\'. Got {2}'.format(cls, self._get_allowed_base_models()))
        return True

    def is_allowed_base_model_instance(self, inst, additional_base_model_class=None):
        """Returns True or raises an exception if the class is an instance of a base model class allowed for serialization."""
        if not isinstance(inst, self._get_allowed_base_models(additional_base_model_class)):
            raise ControllerBaseModelError('For dispatch, user model \'{0}\' must be an instance of \'{1}\'. Got {2}'.format(inst, self._get_allowed_base_models(), inst.__class__))
        return True

    def _get_allowed_base_models(self, additional_base_model_class=None):
        """Returns a tuple of base model classes that may be serialized to json."""
        base_model_class = self.get_allowed_base_models()
        if not isinstance(base_model_class, list):
            raise TypeError('Expected list of base_model classes.')
        if additional_base_model_class:
            if not isinstance(additional_base_model_class, (list, tuple)):
                additional_base_model_class = [additional_base_model_class]
            base_model_class = base_model_class + additional_base_model_class
        base_model_class = base_model_class + [BaseListModel, BaseLabListModel, BaseLabListUuidModel, VisitDefinition, StudySite, BaseHistoryModel, BaseEntryBucket]
        return tuple(base_model_class)

    def get_allowed_base_models(self):
        """Returns a list of base model classes that may be serialized to json.

        Users may override

        This is evaluated in method :func:`_to_json` before serializing an instance. """
        return []

    def _get_base_models_for_default_serialization(self):
        """Wraps :func:`get_allowed_base_models`."""
        base_model_class = self.get_base_models_for_default_serialization()
        if not isinstance(base_model_class, list):
            raise TypeError('Expected base_model classes as a list. Got{0}'.format(base_model_class))
        base_model_class = base_model_class + [BaseListModel, BaseLabListModel, BaseLabListUuidModel, VisitDefinition, StudySite, BaseHistoryModel, BaseEntryBucket]
        return tuple(set(base_model_class))

    def get_base_models_for_default_serialization(self):
        """Returns a tuple of base models from which subclasses should use the
        default method :func:`_to_json` and not a callback from the sender.

        This is evaluated when serializing the foreign keys on an instance and
        you need to know if you can use the callback to serialize the foreign key
        or not."""
        return []

    def get_fk_dependencies(self, instances):
        """Updates the list of foreign key instances required for serialization of the provided instances."""
        for obj in instances:
            for field in obj._meta.fields:
                if isinstance(field, (ForeignKey, OneToOneField)):
                    pk = getattr(obj, field.attname)
                    cls = field.rel.to
                    if (cls, pk) not in self.get_session_container('fk_dependencies'):
                        if cls.objects.filter(pk=pk):
                            this_fk = cls.objects.get(pk=pk)
                            self.fk_instances.append(cls.objects.get(pk=pk))
                            self.get_fk_dependencies([this_fk])
                        self._add_to_session_container((cls, pk), 'fk_dependencies')

    def _disconnect_signals(self, obj):
        """Disconnects signals before saving the serialized object in _to_json."""
        signals.post_save.disconnect(serialize_on_save, weak=False, dispatch_uid="serialize_on_save")
        signals.post_save.disconnect(tracker_on_post_save, weak=False, dispatch_uid="tracker_on_post_save")
        signals.post_save.disconnect(base_visit_tracking_add_or_update_entry_buckets_on_post_save, weak=False, dispatch_uid="base_visit_tracking_add_or_update_entry_buckets_on_post_save")
        signals.post_save.disconnect(base_visit_tracking_on_post_save, weak=False, dispatch_uid="base_visit_tracking_on_post_save")
        self.disconnect_audit_trail_signals(obj)
        self.disconnect_signals()

    def disconnect_signals(self):
        """Disconnects signals before saving the serialized object in _to_json.

        Users may override to add additional signals"""
        pass

    def _reconnect_signals(self):
        """Reconnects signals after saving the serialized object in _to_json."""
        signals.post_save.connect(base_visit_tracking_on_post_save, weak=False, dispatch_uid="base_visit_tracking_on_post_save")
        signals.post_save.connect(base_visit_tracking_add_or_update_entry_buckets_on_post_save, weak=False, dispatch_uid="base_visit_tracking_add_or_update_entry_buckets_on_post_save")
        signals.post_save.connect(tracker_on_post_save, weak=False, dispatch_uid="tracker_on_post_save")
        signals.post_save.connect(serialize_on_save, weak=False, dispatch_uid="serialize_on_save")
        self.reconnect_audit_trail_signals()
        self.reconnect_signals()

    def reconnect_signals(self):
        """Reconnects signals after saving the serialized object in _to_json.

        Users may override to add additional signals"""
        pass

    def get_signal_by_dispatch_uid(self, dispatch_uid):
        signal = None
        for receiver_signal in signals.post_save.receivers:
            if str(receiver_signal[0][0]) == dispatch_uid:
                signal = receiver_signal
                break
        return signal

    def set_audit_trail_signals_for_model(self, obj):
        self.audit_signals = []
        for dispatch_uid in ['audit_serialize_on_save_{0}audit'.format(obj._meta.object_name.lower()), 'audit_on_save_{0}audit'.format(obj._meta.object_name.lower())]:
            audit_signal = self.get_signal_by_dispatch_uid(dispatch_uid)
            if audit_signal:
                self.audit_signals.append(audit_signal)

    def get_audit_trail_signals_for_model(self):
        if not self.audit_signals:
            raise AttributeError('Attribute \'audit_signals\' cannot be None. Call set first.')
        return self.audit_signals

    def disconnect_audit_trail_signals(self, obj):
        self.set_audit_trail_signals_for_model(obj)
        for audit_signal in self.audit_signals:
            signals.post_save.receivers.remove(audit_signal)

    def reconnect_audit_trail_signals(self):
        for audit_signal in self.audit_signals:
            signals.post_save.receivers.append(audit_signal)
        self.audit_signals = None

    def _add_to_session_container(self, instance, key):
        if instance not in self._session_container[key]:
            self._session_container[key].append(instance)

    def get_session_container(self, key):
        return self._session_container[key]

    def in_session_container(self, instance, key):
        if instance in self.get_session_container(key):
            return True
        return False

    def _to_json(self, model_instances, additional_base_model_class=None, to_json_callback=None, user_container=None):
        """Serialize model instances on source to destination.

        Args:
            model_instances: a model instance, list of model instances, or QuerySet
            additional_base_model_class: add a single or list of additional Base classes that the model instances inherit from.
                use sparingly.

        ..warning:: This method assumes you have confirmed that the model_instances are "already dispatched" or not.

        """
        # use default callback (_to_json) if not provided or no user_container
        if not to_json_callback or not user_container:
            # note: foreign keys on containers are not registered w/ dispatch
            to_json_callback = self._to_json
        # check for pending transactions
        if self.has_outgoing_transactions():
            raise PendingTransactionError('Producer \'{0}\' has pending outgoing transactions. Run bhp_sync first.'.format(self.get_producer_name()))
        if self.has_incoming_transactions(model_instances):
            raise PendingTransactionError('Producer \'{0}\' has pending incoming transactions on this server. Consume them first.'.format(self.get_producer_name()))
        if model_instances:
            # convert to list if not iterable
            if not isinstance(model_instances, (list, QuerySet)):
                model_instances = [model_instances]
            if isinstance(model_instances, QuerySet):
                model_instances = [m for m in model_instances]
            # confirm all model_instances are of the correct base class
            for instance in model_instances:
                if self.is_allowed_base_model_instance(instance, additional_base_model_class):
                    # only need to check one as all are of the same class so jump out...
                    break
            # add foreign key instances to the list of model instances to serialize
            while True:
                self.get_fk_dependencies(model_instances)
                break
            model_instances = self.fk_instances + model_instances
            model_instances = list(set(model_instances))
            # skip instances that have already been dispatched during this session
            model_instances = [inst for inst in model_instances if inst not in self.get_session_container('serialized')]
            #serialize
            if model_instances:
                json = serializers.serialize('json', model_instances, use_natural_keys=True)
                deserialized_objects = list(serializers.deserialize("json", json, use_natural_keys=True))
                saved = []
                tries = 0
                while True:
                    tries += 1
                    for deserialized_object in deserialized_objects:
                        try:
                            if deserialized_object not in saved:
                                self._disconnect_signals(deserialized_object.object)
                                deserialized_object.object.save(using=self.get_using_destination())
                                self._reconnect_signals()
                                saved.append(deserialized_object)
                                self._add_to_session_container(instance, 'serialized')
                        except IntegrityError as e:
                            self._reconnect_signals()
                            #print '{0} {1}'.format(e, deserialized_object.object.__class__)
                            continue
                    if len(saved) == len(deserialized_objects):
                        break
                    if tries > 20:
                        raise DeserializationError('Unable to deserialize objects. Tries exceeded on {0}.'.format(deserialized_object.object.__class__))
                    #self.serialize_m2m(d_obj, user_container, to_json_callback)

    def serialize_dependencies(self, d_obj, user_container, to_json_callback):
        # check for foreign keys and, if found, send using the callback
        # Ensures the sent instance is complete / stable
        # TODO: any issue about natural keys?? this searched the destination on pk.
        self.serialize_m2m(d_obj, user_container, to_json_callback)

    def serialize_m2m(self, d_obj, user_container, to_json_callback):
        # check for M2M. If found, populate the list table, then add the list items
        # to the m2m field. See https://docs.djangoproject.com/en/dev/topics/db/examples/many_to_many/
        for m2m_rel_mgr in d_obj.object._meta.many_to_many:
            pk = getattr(d_obj.object, 'pk')
            # get class of this model
            cls = d_obj.object.__class__
            # get instance of this model on source
            inst = cls.objects.get(pk=pk)
            # get the name of the m2m attribute. Note, this is not a model field but a manager
            m2m = m2m_rel_mgr.name
            # try something like test_item_m2m.m2m.all(), gets all() list_model instances for this m2m
            m2m_qs = getattr(inst, m2m).all()
            # create list_model instances on destination if they do not exist
            dst_list_item_pks = []
            for src_list_item in m2m_qs:
                if not src_list_item.__class__.objects.using(self.get_using_destination()).filter(pk=src_list_item.pk).exists():
                    # no need to use callback, list models are not registered with dispatch
                    self._to_json(src_list_item, additional_base_model_class=BaseListModel)
                    # record source pk for use later
                    # TODO: confirm the pk on source is always the same on destination? what about natural keys?
                    dst_list_item_pks.append(src_list_item.pk)
            # get instance of this model on destination
            inst = cls.objects.using(self.get_using_destination()).get(pk=pk)
            # find the pk for each list model instance and add to the m2m "field"
            for pk in dst_list_item_pks:
                # get the list_model instance on destination
                item_inst = src_list_item.__class__.objects.using(self.get_using_destination()).get(pk=pk)
                # add to m2m rel_manager on destination, this is like instance.m2m.add(item)
                getattr(inst, m2m).add(item_inst)

                    # TODO: commented out below so we can see the errors in testing
                    #       May need to uncomment before release
    
    #                except IntegrityError as e:
    #                    logger.info(e)
    #                    logger.info(e.message)
    #                    if 'is not unique' in e.message:
    #                        raise DispatchError('Model instance {0} is already on producer {1}.'.format(d_obj.object, self.get_producer_name()))
    #                    if 'Duplicate' in e.message:
    #                        pass
    #                    elif 'Cannot add or update a child row' in e.message:
    #                        # assume Integrity error was because of missing ForeignKey data
    #                        self.dispatch_foreign_key_instances(self.get_dispatch_item_app_label())
    #                        # try again
    #                        # disconnect signal
    #                        signals.post_save.disconnect(serialize_on_save, weak=False, dispatch_uid="serialize_on_save")
    #                        #save
    #                        d_obj.save(using=self.get_using_destination())
    #                        # reconnect
    #                        signals.post_save.connect(serialize_on_save, weak=False, dispatch_uid="serialize_on_save")
    #                    else:
    #                        raise
    #                except:
    #                    raise
