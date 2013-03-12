import logging
from django.core import serializers
from django.db import IntegrityError
from django.db.models.query import QuerySet
from django.db.models import get_models, get_app, ForeignKey, OneToOneField, signals
from bhp_sync.models import BaseSyncUuidModel
from bhp_sync.models.signals import serialize_on_save
from bhp_sync.exceptions import PendingTransactionError
from bhp_dispatch.exceptions import DispatchModelError, AlreadyDispatchedItem, AlreadyReturnedController, DispatchError, DispatchContainerError, AlreadyDispatchedContainer
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
        if not self.get_dispatch_container_register_instance().is_dispatched:
            raise AlreadyReturnedController('This controller has already returned it\'s items. To dispatch new items, create a new instance.')
        if not isinstance(user_container, BaseSyncUuidModel):
            raise DispatchContainerError('User container must be an instance of BaseSyncUuidModel')
        if not user_container.is_dispatch_container_model():
            raise DispatchContainerError('Model {0} is not configured as a dispatch container model'.format(user_container))
        # confirm not already dispatched as item
        if user_container.is_dispatched_as_item():
            raise AlreadyDispatchedItem('Item is already dispatched. Got {0}.'.format(user_container))
        # dispatch
        self._dispatch_as_json([user_container])
        if not self.register_with_dispatch_item_register(user_container):
            raise DispatchError('Unable to create a dispatch item register for user container {0} {1} to {2}.'.format(user_container._meta.object_name, user_container.object, self.get_using_destination()))
        logger.info('dispatched {0} {1} to {2}.'.format(user_container._meta.object_name, user_container, self.get_using_destination()))

    def dispatch_user_items_as_json(self, user_items, user_container=None):
        if not self.get_dispatch_container_register_instance().is_dispatched:
            raise AlreadyReturnedController('This controller has already returned it\'s items. To dispatch new items, create a new instance.')
        user_container = user_container or self.get_user_container_instance()
        # confirm no user_items are already dispatched (but send with user_container to skip the "dispatched within container" check)
        already_dispatched_items = [user_instance for user_instance in user_items if user_instance.is_dispatched_as_item(user_container=user_container)]
        if already_dispatched_items:
            raise AlreadyDispatchedItem('{0} models are already dispatched. Got {1}'.format(len(already_dispatched_items), already_dispatched_items))
        # dispatch
        self._dispatch_as_json(user_items)
        # register the user items with the dispatch item register
        for user_item in user_items:
            if not self.register_with_dispatch_item_register(user_item, user_container):
                raise DispatchError('Unable to create a dispatch item register instance for {0} {1} to {2}.'.format(user_item._meta.object_name, user_item.object, self.get_using_destination()))
            logger.info('dispatched {0} {1} to {2}.'.format(user_item._meta.object_name, user_item, self.get_using_destination()))

    def _dispatch_as_json(self, model_instances):
        self._to_json(model_instances)
