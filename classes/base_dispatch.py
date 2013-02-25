import logging
import socket
from django.conf import settings
from django.db.models import get_model, ForeignKey, OneToOneField
from django.core.exceptions import ImproperlyConfigured
from bhp_visit.models import MembershipForm
from django.db.models.query import QuerySet
from django.core import serializers
from django.db import IntegrityError
from datetime import datetime
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
        """Creates a dispatch container instance for this controller sessions."""
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
        """Creates an instance of DispatchItem for an item being dispatched."""
        if instance._meta.app_label not in settings.DISPATCH_APP_LABELS and not instance.include_for_dispatch():
            raise ImproperlyConfigured('Model {0} is not configured for dispatch. See model method \'include_for_dispatch\'  or settings attribute DISPATCH_APP_LABELS.'.format(instance._meta.object_name))
        if not instance.is_dispatched:
            try:
                dispatch_item = DispatchItem.objects.create(
                    dispatch_container=self.get_dispatch_container_instance(),
                    producer=self.get_producer(),
                    item_app_label=instance._meta.app_label,
                    item_model_name=instance._meta.object_name,
                    item_pk=instance.pk,
                    item_identifier_attrname=self.get_dispatch_item_identifier_attrname(),
                    item_identifier=getattr(instance, self.get_dispatch_item_identifier_attrname()),
                    dispatch_using=settings.DATABASES.get(self.get_using_source()).get('name'),
                    dispatch_host=socket.gethostname(),
                    is_dispatched=True)
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

    def return_from_producer(self, producer, source_instances=None, **kwargs):
        msgs = []
        if self.has_outgoing_transactions():
            raise PendingTransactionError('Producer \'{0}\' has pending outgoing transactions. Run bhp_sync first.'.format(self.get_producer_name()))
        if self.has_incoming_transactions(source_instances):
            raise PendingTransactionError('Producer \'{0}\' has pending incoming transactions on this server. Consume them first.'.format(self.get_producer_name()))
        else:
            container_instances = DispatchContainer.objects.filter(producer=producer, is_dispatched=True)
            if container_instances.count() > 0:
                for container in container_instances:
                    #dispatched_models = container.get_dispatched_items_for_container()
                    dispatched_models = DispatchItem.objects.filter(dispatch_container=container)
                    for dispatched_model in dispatched_models:
                        dispatched_model.return_datetime = datetime.now()
                        dispatched_model.is_dispatched = False
                        dispatched_model.save()
                    container.is_dispatched = False
                    container.return_datetime = datetime.now()
                    container.save()
                    #dispatched_models.delete()  
                    msgs.append('Returned {0} items of {1} with {2}={3}'.format(dispatched_models.count(),
                                                                                container.container_model_name,
                                                                                container.container_identifier_attrname,
                                                                                container.container_identifier))
            else:
                msgs.append('Nothing to return. There are no current dipatched items.')
        return msgs

#    def dispatch_model_as_json(self, models, **kwargs):
#        # TODO: what is the difference betweeen this and dispatch_as_json??
#        """Serializes and saves all instances of each model from source to destination.
#
#            Args:
#                models: may be a tuple of (app_name, model_name) or list of model classes.
#        """
#        # TODO: when would this NOT be a subclass of BaseSyncUuidModel??
#        base_model_class = kwargs.get('base_model_class', BaseSyncUuidModel)
#        use_natural_keys = kwargs.get('use_natural_keys', True)
#        select_recent = kwargs.get('select_recent', True)
#        #check_transactions = kwargs.get('check_transactions', True)
#        #if check_transactions:
#        if not models:
#            raise DispatchModelError('Parameter \'models\' may not be None.')
#        # if models is a tuple, convert to model class using get_model
#        if isinstance(models, tuple):
#            mdl = get_model(models[self.APP_NAME], models[self.MODEL_NAME])
#            if not mdl:
#                raise self.exception('Unable to get_model() using app_name={0}, model_name={1}.'.format(models[self.APP_NAME], models[self.MODEL_NAME]))
#            models = mdl
#        # models must be a list
#        if not isinstance(models, (list,)):
#            models = [models]
#        if self.has_outgoing_transactions():
#            raise PendingTransactionError('Producer \'{0}\' has pending outgoing transactions. Run bhp_sync first.'.format(self.get_producer_name()))
#        if self.has_incoming_transactions(models):
#            raise PendingTransactionError('Producer \'{0}\' has pending incoming transactions on this server. Consume them first.'.format(self.get_producer_name()))
#
#        for model in models:
#            if not issubclass(model, base_model_class):
#                raise DispatchModelError('Dispatch model {0} must be an instance of \'{1}\'.'.format(model, base_model_class))
#            if not select_recent:
#                source_queryset = model.objects.using(self.get_using_source()).all().order_by('id')
#            else:
#                source_queryset = self.get_recent(model)
#            tot = source_queryset.count()
#
#            logger.info('    saving {0} instances for {1} on {2}.'.format(tot, model._meta.object_name, self.get_using_destination()))
#            json = serializers.serialize('json', source_queryset, use_natural_keys=use_natural_keys)
#            n = 0
#            if json:
#                try:
#                    for obj in serializers.deserialize("json", json):
#                        n += 1
#                        try:
#                            # disconnect signal to avoid creating transactions on the source for data saved on destination
#                            signals.post_save.disconnect(serialize_on_save, weak=False, dispatch_uid="serialize_on_save")
#                            obj.save(using=self.get_using_destination())
#                            signals.post_save.connect(serialize_on_save, weak=False, dispatch_uid="serialize_on_save")
#                        except IntegrityError:
#                            logger.info('    skipping. Duplicate detected for {0} (a).'.format(obj))
#                except DeserializationError:
#                    for instance in source_queryset:
#                        json = serializers.serialize('json', [instance], use_natural_keys=True)
#                        try:
#                            for obj in serializers.deserialize("json", json):
#                                n += 1
#                                try:
#                                    # disconnect signal to avoid creating transactions on the source for data saved on destination
#                                    signals.post_save.disconnect(serialize_on_save, weak=False, dispatch_uid="serialize_on_save")
#                                    obj.save(using=self.get_using_destination())
#                                    signals.post_save.connect(serialize_on_save, weak=False, dispatch_uid="serialize_on_save")
#                                except IntegrityError:
#                                    logger.info('    skipping. Duplicate detected for {0} (b).'.format(obj))
#                        except:
#                            logger.info('    SKIPPING {0}'.format(instance._meta.object_name))
#            logger.info('    done. saved {0} / {1} for model {2}'.format(n, tot, model._meta.object_name))


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
