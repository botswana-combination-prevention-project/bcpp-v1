import logging
import socket
from django.conf import settings
from django.db.models import get_model, ForeignKey, OneToOneField
from django.core.exceptions import ImproperlyConfigured
from bhp_visit.models import MembershipForm
from django.db.models.query import QuerySet
from django.core import serializers
from django.db import IntegrityError
from bhp_sync.models import BaseSyncUuidModel
from bhp_sync.models.signals import serialize_on_save
from bhp_sync.exceptions import PendingTransactionError
from bhp_dispatch.exceptions import DispatchModelError, DispatchError
from bhp_dispatch.models import DispatchItem, DispatchContainer
from base import Base

logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class BaseDispatch(Base):
    """A model is tracked as dispatched by a instance in DispatchItem searchable on its pk, app_label, model_name.

    Additionally, a model can be configured as a container model so that the DispatchContainer makes reference to it.

    All models are tacked in DispatchItem. Container models are also referenced in DispatchContainer.

    """
    def __init__(self,
                 using_source,
                 using_destination,
                 dispatch_container_app_label,
                 dispatch_container_model_name,
                 dispatch_container_identifier_attrname,
                 dispatch_container_identifier,
                 **kwargs):
        super(BaseDispatch, self).__init__(using_source, using_destination, **kwargs)
        self._dispatch_item_model_name = None
        self._dispatch_container_app_label = None
        self._dispatch_container_identifier_attrname = None
        self._dispatch_container_identifier = None
        self._dispatch = None
        self._visit_models = {}
        self._set_dispatch_container_app_label(dispatch_container_app_label)
        self._set_dispatch_container_model_name(dispatch_container_model_name)
        self._set_dispatch_container_identifier_attrname(dispatch_container_identifier_attrname)
        self.set_dispatch_container_identifier(dispatch_container_identifier)
        self._set_dispatch_container_instance()
        self.debug = kwargs.get('debug', False)

    def _set_dispatch_container_model_name(self, value):
        if not value:
            raise AttributeError('The model_name of the dispatch container cannot be None. Set this in __init__() of the subclass.')
        self._dispatch_container_model_name = value

    def get_dispatch_container_model_name(self):
        """Gets the model name for the dispatching item."""
        if not self._dispatch_container_model_name:
            self._set_dispatch_container_model_name()
        return self._dispatch_container_model_name

    def get_dispatch_item_identifier_attrname(self):
        return 'id'

    def _set_dispatch_container_app_label(self, value):
        if not value:
            raise AttributeError('The app_label of the dispatch container model cannot be None. Set this in __init__() of the subclass.')
        self._dispatch_container_app_label = value

    def get_dispatch_container_app_label(self):
        """Gets the app_label for the dispatching container."""
        if not self._dispatch_container_app_label:
            self._set_dispatch_container_app_label()
        return self._dispatch_container_app_label

    def _set_dispatch_container_identifier_attrname(self, value=None):
        """Sets identifier field attribute of the dispatch model.

        This is an identifier for the model thats the starting point of dispatching
        e.g household_identifier if starting with household or subject identifier if starting with registered subject.

        This identifier will be determined by the application specific controller/model sub classing a base model
        e.g MochudiDispatchController or mochudi_household
        """
        if not value:
            raise AttributeError('The identifier field of the dispatch model cannot be None. Set this in __init__() of the subclass.')
        self._dispatch_container_identifier_attrname = value

    def get_dispatch_container_identifier_attrname(self):
        """Gets the item identifier for the dispatching model."""
        if not self._dispatch_container_identifier_attrname:
            self._set_dispatch_container_identifier_attrname()
        return self._dispatch_container_identifier_attrname

    def set_dispatch_container_identifier(self, value=None):
        if not value:
            raise AttributeError('The identifier of the user\'s dispatch container model instance cannot be None.')
        self._dispatch_container_identifier = value

    def get_dispatch_container_identifier(self):
        """Gets the identifier for the user's dispatch container instance."""
        if not self._dispatch_container_identifier:
            self.set_dispatch_container_identifier()
        return self._dispatch_container_identifier

    def _set_dispatch_container_instance(self):
        """Creates a dispatch container instance for this controller session."""
        user_dispatch_container_model = get_model(self.get_dispatch_container_app_label(), self.get_dispatch_container_model_name())
        if not user_dispatch_container_model.objects.filter(**{self.get_dispatch_container_identifier_attrname(): self.get_dispatch_container_identifier()}):
            raise DispatchModelError('Cannot set container model instance. Container model {0} matching query does not exist for {1}=\'{2}\'.'.format(user_dispatch_container_model._meta.object_name, self.get_dispatch_container_identifier_attrname(), self.get_dispatch_container_identifier()))
        else:
            obj = user_dispatch_container_model.objects.get(**{self.get_dispatch_container_identifier_attrname(): self.get_dispatch_container_identifier()})
        if not getattr(obj, self.get_dispatch_container_identifier_attrname()):
            raise DispatchError('Attribute {0} not found on model instance {1}.'.format(self.get_dispatch_container_identifier_attrname(), self.get_dispatch_container_model_name()))
        self._dispatch_container = DispatchContainer.objects.create(
            producer=self.get_producer(),
            is_dispatched=True,
            container_app_label=self.get_dispatch_container_app_label(),
            container_model_name=self.get_dispatch_container_model_name(),
            container_identifier_attrname=self.get_dispatch_container_identifier_attrname(),
            container_identifier=getattr(obj, self.get_dispatch_container_identifier_attrname()),
            container_pk=obj.pk)
        # update the dispatch_items queryset
        #TODO: probably remove this
        self.set_dispatched_items_for_container()

    def get_dispatch_container_instance(self):
        """Gets the dispatch container instance for this controller sessions."""
        if not self._dispatch_container:
            self._set_dispatch_container_instance()
        return self._dispatch_container

    def set_dispatched_items_for_producer(self):
        """Sets a queryset of dispatched DispatchItem model instances for the current producer."""
        self._dispatched_items_for_producer = DispatchItem.objects.using(self.get_using_source()).filter(
            producer=self.get_producer(),
            is_dispatched=True,
            return_datetime__isnull=True)

    def get_dispatched_items_for_producer(self):
        """Returns a queryset of dispatched DispatchItem model instances for this producer."""
        if not self._dispatched_items_for_producer:
            self.set_dispatched_items_for_producer()
        return self._dispatched_items_for_producer

    def set_dispatched_items_for_container(self):
        """Sets a queryset of dispatched DispatchItem model instances for the current container."""
        self._dispatched_items_for_container = DispatchItem.objects.using(self.get_using_source()).filter(
            dispatch_container=self.get_dispatch_container_instance(),
            is_dispatched=True,
            return_datetime__isnull=True)

    def get_dispatched_items_for_container(self):
        """Returns a queryset of dispatched DispatchItem model instances for this container."""
        if not self._dispatched_items_for_container:
            self.set_dispatched_items_for_container()
        return self._dispatched_items_for_container

    def set_producer(self):
        super(BaseDispatch, self).set_producer()
        # producer has changed so update the list of
        # dispatched Dispatch items instances for this producer
        #TODO: probably remove this
        self.set_dispatched_items_for_producer()

    def create_dispatched_item_instance(self, instance):
        """Creates an instance of DispatchItem for an item being dispatched.

        ...note: If an instance of dispatch item already exists it will be reused (get_or_create)"""
        if instance._meta.app_label not in settings.DISPATCH_APP_LABELS and not instance.include_for_dispatch():
            raise ImproperlyConfigured('Model {0} is not configured for dispatch. See model method \'include_for_dispatch\'  or settings attribute DISPATCH_APP_LABELS.'.format(instance._meta.object_name))
        if not instance.is_dispatched:
            try:
                defaults = {
                    'is_dispatched': True,
                    'producer': self.get_producer(),
                    'dispatch_host': socket.gethostname(),
                    'dispatch_using': settings.DATABASES.get(self.get_using_source()).get('name'),
                    'item_app_label': instance._meta.app_label,
                    'item_model_name': instance._meta.object_name,
                    'item_identifier_attrname': self.get_dispatch_item_identifier_attrname(),
                    }
                dispatch_item, created = DispatchItem.objects.get_or_create(
                    dispatch_container=self.get_dispatch_container_instance(),
                    item_identifier=getattr(instance, self.get_dispatch_item_identifier_attrname()),
                    item_pk=instance.pk,
                    defaults=defaults)
                if not created:
                    dispatch_item.is_dispatched = True
                    dispatch_item.return_datetime = None
                    dispatch_item.producer = self.get_producer()
                    dispatch_item.dispatch_host = socket.gethostname()
                    dispatch_item.dispatch_using = settings.DATABASES.get(self.get_using_source()).get('name')
                    dispatch_item.item_app_label = instance._meta.app_label
                    dispatch_item.item_model_name = instance._meta.object_name
                    dispatch_item.item_identifier_attrname = self.get_dispatch_item_identifier_attrname()
                    dispatch_item.save()
            except IntegrityError:
                raise ImproperlyConfigured('Attempting to dispatch a model that is not \"dispatchable\". Expected instance.is_dispatched=True for Model{0}. Please check that this model has method \'include_for_dispatch()\' or model\'s app_label is included in settings.DISPATCH_APP_LABELS'.format(instance._meta.object_name))
            return dispatch_item
        return False

    def get_membershipform_models(self):
        """Returns a list of 'visible' membership form model classes."""
        return [membership_form.content_type_map.content_type.model_class() for membership_form in MembershipForm.objects.using(self.get_using_source()).filter(visible=True)]

    def set_visit_model_cls(self, app_label, model_cls):
        """Sets the visit_model_cls attribute with a dictionary of tuples (field name, class) by app.
        """
        from bhp_visit_tracking.models import BaseVisitTracking
        self._visit_models = {}
        if not model_cls:
            raise TypeError('Parameter model_cls cannot be None.')
        for field in model_cls._meta.fields:
            if isinstance(field, (ForeignKey, OneToOneField)):
                field_cls = field.rel.to
                if issubclass(field_cls, BaseVisitTracking):
                    # does this dict ever have more than one entry??
                    self._visit_models.update({app_label: (field.name, field_cls)})

    def get_visit_model_cls(self, app_label, model_cls=None, **kwargs):
        """Returns a tuple of (field name, class) or just one of the tuple items.

        Keywords:
            index: either 'name' or 'cls'. If specified, only returns the item in the tuple instead of the whole tuple.
        """
        if not self._visit_models.get(app_label):
            self.set_visit_model_cls(app_label, model_cls)
        # check for kwarg 'key' and set key to 0 or 1 (or None if not found)
        index = {'name': 0, 'cls': 1}.get(kwargs.get('index', None), None)
        if not self._visit_models.get(app_label):
            tpl = (None, None)
        else:
            tpl = self._visit_models.get(app_label)
        if index in [0, 1]:
            return tpl[index]
        else:
            return tpl
