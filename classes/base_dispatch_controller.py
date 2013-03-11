import logging
from django.core import serializers
from django.db import IntegrityError
from django.db.models.query import QuerySet
from django.db.models import get_models, get_app, ForeignKey, OneToOneField, signals
from bhp_sync.models import BaseSyncUuidModel
from bhp_sync.models.signals import serialize_on_save
from bhp_sync.exceptions import PendingTransactionError
from bhp_dispatch.exceptions import DispatchModelError, AlreadyDispatchedItem, DispatchError, DispatchContainerError
from bhp_dispatch.models import DispatchContainerRegister
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
                 user_container_app_label,
                 user_container_model_name,
                 user_container_identifier_attrname,
                 user_container_identifier,
                 dispatch_item_app_label,
                 **kwargs):
        self._dispatch_item_app_label = None
        #self._set_dispatch_item_app_label(dispatch_item_app_label)
        super(BaseDispatchController, self).__init__(
            using_source,
            using_destination,
            user_container_app_label,
            user_container_model_name,
            user_container_identifier_attrname,
            user_container_identifier,
            **kwargs)
        self._dispatch_list = []

#    def _set_dispatch_item_app_label(self, value):
#        if not value:
#            raise AttributeError('The app_label of the dispatching item model cannot be None. Set this in __init__() of the subclass.')
#        self._dispatch_item_app_label = value
#
#    def get_dispatch_item_app_label(self):
#        """Gets the app_label for the dispatching item."""
#        if not self._dispatch_item_app_label:
#            self._set_dispatch_item_app_label()
#        return self._dispatch_item_app_label

    def dispatch_foreign_key_instances(self):
        """Finds foreign_key model classes other than the visit model class and exports the instances."""
        list_models = []
        
        #TODO: should only work for list models so that it does not cascade into all data
        app_label = self.get_dispatch_item_app_label()
        if not app_label:
            raise TypeError('Parameter app_label cannot be None.')
        app = get_app(app_label)
        for model_cls in get_models(app):
            # TODO: this could be wrong visit_field_name?
            try:
                visit_field_name = self.get_visit_model_cls(app_label, model_cls, index='name')
                if getattr(model_cls, visit_field_name, None):
                    for field in model_cls._meta.fields:
                        if not field.name == visit_field_name and isinstance(field, (ForeignKey, OneToOneField)):
                            field_cls = field.rel.to
                            if field_cls not in list_models:
                                list_models.append(field_cls)
            except:
                pass
        logger.info('Ready to dispatch foreign keys: {0}'.format(list_models))
        for model_cls in list_models:
            self.dispatch_model_as_json(model_cls.objects.using(self.get_using_source()).all(), self.get_user_container_instance(), app_label=app_label)

    def get_scheduled_models(self, app_label):
        """Returns a list of model classes with a foreign key to the visit model for the given app, excluding audit models."""
        app = get_app(app_label)
        scheduled_models = []
        for model_cls in get_models(app):
            field_name, visit_model_cls = self.get_visit_model_cls(app_label, model_cls)
            if visit_model_cls:
                if getattr(model_cls, field_name, None):
                    if not model_cls._meta.object_name.endswith('Audit'):
                        scheduled_models.append(model_cls)
        return scheduled_models

    def dispatch_model_as_json(self, model_cls, user_container=None):
        """Dispatch all instances of a model class.

           Args:
                user_container: instance of model used as the container. Note items may not
                                    may not be dispatched without a container.
                model_cls: a subclass of BaseSyncUuidModel"""
        self.dispatch_user_items_as_json(model_cls.objects.all(), user_container)

    def dispatch_user_container_as_json(self, user_container):
        if not isinstance(user_container, BaseSyncUuidModel):
            raise DispatchContainerError('User container must be an instance of BaseSyncUuidModel')
        if not user_container.is_dispatch_container_model():
            raise DispatchContainerError('Model {0} is not configured as a dispatch container model'.format(user_container))
        self._dispatch_as_json([user_container])
        if not self.register_with_dispatch_item_register(user_container):
            raise DispatchError('Unable to create a dispatch item register for user container {0} {1} to {2}.'.format(user_container._meta.object_name, user_container.object, self.get_using_destination()))
        logger.info('dispatched {0} {1} to {2}.'.format(user_container._meta.object_name, user_container, self.get_using_destination()))

    def dispatch_user_items_as_json(self, user_items, user_container=None):
        user_container = user_container or self.get_user_container_instance()
        #if not user_container:
        #    raise DispatchError('Attribute user_container may not be None')
        #if isinstance(user_container, DispatchContainerRegister):
        #    raise DispatchError('Attribute user_container cannot be an instance on DispatchContainerRegister')
        self._dispatch_as_json(user_items)
        # register the user items with the dispatch item register
        for user_item in user_items:
            if not self.register_with_dispatch_item_register(user_item, user_container):
                raise DispatchError('Unable to create a dispatch item register instance for {0} {1} to {2}.'.format(user_item._meta.object_name, user_item.object, self.get_using_destination()))
            logger.info('dispatched {0} {1} to {2}.'.format(user_item._meta.object_name, user_item, self.get_using_destination()))

    def _dispatch_as_json(self, source_instances, user_container=None, **kwargs):
        """Serialize models on source and deserialize on destination.

            Args:
                user_container: instance of a model that may be dispatched as a container. Note items may not
                                    may not be dispatched without a container.
                source_instance: a model instance(s) from the source server
        """
        base_model_class = BaseSyncUuidModel
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
                    raise DispatchModelError('For dispatch, user model {0} must be an instance of \'{1}\'.'.format(instance, base_model_class))
            #serialize
            json = serializers.serialize('json', source_instances, use_natural_keys=True)
            # deserialize on destination
            for d_obj in serializers.deserialize("json", json, use_natural_keys=True):
                # TODO: check the using parameter
                if d_obj.object.is_dispatched_as_item():
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
 