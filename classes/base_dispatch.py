import logging
from django.db.models import get_model, get_models, get_app, ForeignKey, OneToOneField
from bhp_visit.models import MembershipForm
from bhp_dispatch.exceptions import DispatchError
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
    def __init__(self, using_source, using_destination, dispatch_container_app_label, dispatch_container_model_name, dispatch_container_identifier_attrname, dispatch_container_identifier, dispatch_item_app_label, **kwargs):
        super(BaseDispatch, self).__init__(using_source, using_destination, **kwargs)
        self._dispatch_item_app_label = None
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
        self._set_dispatch_item_app_label(dispatch_item_app_label)
        self._set_dispatch_container_instance()
        self.debug = kwargs.get('debug', False)

    def _set_dispatch_item_app_label(self, value):
        if not value:
            raise AttributeError('The app_label of the dispatching item model cannot be None. Set this in __init__() of the subclass.')
        self._dispatch_item_app_label = value

    def get_dispatch_item_app_label(self):
        """Gets the app_label for the dispatching item."""
        if not self._dispatch_item_app_label:
            self._set_dispatch_item_app_label()
        return self._dispatch_item_app_label

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
        """Creates a dispatch container instance for this controller sessions."""
        user_dispatch_container_model = get_model(self.get_dispatch_container_app_label(), self.get_dispatch_container_model_name())
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

    def dispatch_foreign_key_instances(self, app_label):
        """Finds foreign_key model classes other than the visit model class and exports the instances."""
        list_models = []
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

    def get_scheduled_models(self, app_label=None):
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

#    def update_lists(self):
#        """Updates all list models on the destination with data from the source.
#        """
#        #Make sure we have a target producer to export lists to
#        if not self.get_producer():
#            raise ValueError("PLEASE specify the producer you want checkout models to!")
#        list_models = []
#        for model in get_models():
#            if issubclass(model, BaseListModel):
#                list_models.append(model)
#        for list_model in list_models:
#            logger.info(list_model._meta.object_name)
#            json = serializers.serialize(
#                'json',
#                list_model.objects.using(self.get_using_source()).all().order_by('name'),
#                use_natural_keys=True
#                )
#
#            for obj in serializers.deserialize("json", json):
#                obj.save(using=self.get_using_destination())
