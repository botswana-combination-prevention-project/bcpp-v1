import logging
from django.core import serializers
from django.db import IntegrityError
from django.db.models.query import QuerySet
from django.db.models import get_models, get_app, ForeignKey, OneToOneField, signals
from bhp_sync.models import BaseSyncUuidModel
from bhp_sync.models.signals import serialize_on_save
from bhp_sync.exceptions import PendingTransactionError
from bhp_dispatch.exceptions import DispatchModelError, AlreadyDispatchedItem, DispatchError
from bhp_dispatch.models import DispatchContainer
from base_dispatch import BaseDispatch


logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class BaseDispatchController(BaseDispatch):

    def __init__(self,
                 using_source,
                 using_destination,
                 dispatch_container_app_label,
                 dispatch_container_model_name,
                 dispatch_container_identifier_attrname,
                 dispatch_container_identifier,
                 dispatch_item_app_label,
                 **kwargs):
        self._dispatch_item_app_label = None
        self._set_dispatch_item_app_label(dispatch_item_app_label)
        super(BaseDispatchController, self).__init__(
            using_source,
            using_destination,
            dispatch_container_app_label,
            dispatch_container_model_name,
            dispatch_container_identifier_attrname,
            dispatch_container_identifier,
            **kwargs)
        self._dispatch_list = []

    def _set_dispatch_item_app_label(self, value):
        if not value:
            raise AttributeError('The app_label of the dispatching item model cannot be None. Set this in __init__() of the subclass.')
        self._dispatch_item_app_label = value

    def get_dispatch_item_app_label(self):
        """Gets the app_label for the dispatching item."""
        if not self._dispatch_item_app_label:
            self._set_dispatch_item_app_label()
        return self._dispatch_item_app_label

    def dispatch_foreign_key_instances(self):
        """Finds foreign_key model classes other than the visit model class and exports the instances."""
        list_models = []
        app_label = self.get_dispatch_item_app_label()
        if not app_label:
            raise TypeError('Parameter app_label cannot be None.')
        app = get_app(app_label)
        for model_cls in get_models(app):
            # TODO: this could be wrong visit_field_name?
            visit_field_name = self.get_visit_model_cls(app_label, model_cls, index='name')
            if getattr(model_cls, visit_field_name, None):
                for field in model_cls._meta.fields:
                    if not field.name == visit_field_name and isinstance(field, (ForeignKey, OneToOneField)):
                        field_cls = field.rel.to
                        if field_cls not in list_models:
                            list_models.append(field_cls)
        logger.info('Ready to dispatch foreign keys: {0}'.format(list_models))
        for model_cls in list_models:
            self.dispatch_model_as_json(model_cls.objects.using(self.get_using_source()).all(), app_label=app_label)

    def get_scheduled_models(self):
        """Returns a list of model classes with a foreign key to the visit model for the given app, excluding audit models."""
        app = get_app(self.get_dispatch_item_app_label())
        scheduled_models = []
        for model_cls in get_models(app):
            field_name, visit_model_cls = self.get_visit_model_cls(self.get_dispatch_item_app_label(), model_cls)
            if visit_model_cls:
                if getattr(model_cls, field_name, None):
                    if not model_cls._meta.object_name.endswith('Audit'):
                        scheduled_models.append(model_cls)
        return scheduled_models

    def dispatch_model_as_json(self, dispatch_container, model_cls):
        base_model_class = BaseSyncUuidModel
        if not issubclass(model_cls, BaseSyncUuidModel):
            raise DispatchModelError('Dispatch model {0} must be a subclass of \'{1}\'.'.format(model_cls, base_model_class))
        self.dispatch_as_json(dispatch_container, [instance for instance in model_cls.objects.all()])

    def dispatch_as_json(self, source_instances, dispatch_container, **kwargs):
        """Serialize a remote model instance, deserialize and save to local instances.

            Args:
                dispatch_container: instance of DispatchContainer. Note items may not
                                    may not be dispatched without a container.
                source_instance: a model instance(s) from the source server
        """
        base_model_class = BaseSyncUuidModel
        dispatch_container = dispatch_container or self.get_dispatch_container_instance()
        if not dispatch_container:
            raise DispatchError('Attribute dispatch_container may not be None')
        if not isinstance(dispatch_container, DispatchContainer):
            raise DispatchError('Attribute dispatch_container must be an instance on DispatchContainer')
        # check for pending transactions
        if self.has_outgoing_transactions():
            raise PendingTransactionError('Producer \'{0}\' has pending outgoing transactions. Run bhp_sync first.'.format(self.get_producer_name()))
        if self.has_incoming_transactions(source_instances):
            raise PendingTransactionError('Producer \'{0}\' has pending incoming transactions on this server. Consume them first.'.format(self.get_producer_name()))
        if source_instances:
            # convert to list if not iterable
            if not isinstance(source_instances, (list, QuerySet)):
                source_instances = [source_instances]
            # confirm all instances are of the correct base class
            for instance in source_instances:
                if not isinstance(instance, base_model_class):
                    raise DispatchModelError('Dispatch model {0} must be an instance of \'{1}\'.'.format(instance, base_model_class))
            #serialize
            json = serializers.serialize('json', source_instances, use_natural_keys=True)
            # deserialize on destination
            for d_obj in serializers.deserialize("json", json, use_natural_keys=True):
                if d_obj.object.is_dispatched:
                    raise AlreadyDispatchedItem('Model {0}-{1} is currently dispatched'.format(d_obj.object._meta.object_name, d_obj.object.pk))
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
                # create_dispatched_item_instance for this dispatched d_obj
                if not self.create_dispatched_item_instance(d_obj.object):
                    raise DispatchError('Unable to create a dispatch item instance for {0} {1} to {2}.'.format(d_obj.object._meta.object_name, d_obj.object, self.get_using_destination()))
                logger.info('dispatched {0} {1} to {2}.'.format(d_obj.object._meta.object_name, d_obj.object, self.get_using_destination()))
