import logging
import copy
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_model
from bhp_sync.models import BaseSyncUuidModel
from bhp_dispatch.exceptions import AlreadyDispatchedContainer, AlreadyDispatchedItem, DispatchError
#from bhp_dispatch.models import DispatchItem, DispatchContainer


logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class BaseDispatchSyncUuidModel(BaseSyncUuidModel):

    """Base model for all UUID models and adds dispatch methods and signals. """

    def is_dispatch_container_model(self):
        """Flags a model as a container model that if dispatched will not appear in DispatchItems, but rather in DispatchContainer."""
        return False

    def ignore_for_dispatch(self):
        """Flgas a model to be ignored by the dispatch infrastructure.

        ..note:: only use this for models that exist in an app listed in the settings.DISPATCH_APP_LABELS but need to be ignored (which should not be very often)."""
        return False

    def include_for_dispatch(self):
        """Flgas a model to be included by the dispatch infrastructure.

        ..note:: only use this for models that do not exist in an app listed in the settings.DISPATCH_APP_LABELS but need to be included (which should not be very often)."""
        return False

    def is_dispatchable_model(self):
        if self.ignore_for_dispatch():
            return False
        if not self._meta.app_label in settings.DISPATCH_APP_LABELS:
            if self.include_for_dispatch():
                return True
            else:
                return False
        return True

    @property
    def is_dispatched(self):
        """Returns True if the model is tracked/is_dispatched=True in the DispatchItem model.

        ..note:: Unlike, :func:`_is_dispatched_to_producer_as_container`, this method does NOT consider
            DispacthContainer. So if the instance is referred to in DispacthContainer but
            not yet tracked in the DispatchItem model, the return value is False."""
        is_dispatched = False
        if self.is_dispatchable_model():
            is_dispatched = self.is_dispatched_as_item()
            if not isinstance(is_dispatched, bool):
                raise TypeError('Expected a boolean as a return value from method is_dispatched_as_item(). Got {0}'.format(is_dispatched))
        return is_dispatched

    def dispatched_as_container_identifier_attr(self):
        """Override to return the field attrname of the identifier used for the dispatch container.

        Must be an field attname on the model used as a dispatch container, such as, household_identifier on model Household."""
        raise ImproperlyConfigured('Method must be overridden on model {0}'.format(self._meta.object_name))

    def _is_dispatched_as_container(self, using=None):
        """Determines if a model instance is dispatched as a container.

        For example: a household model instance may serve as a container for all household members and data."""
        is_dispatched = False
        DispatchContainer = get_model('bhp_dispatch', 'DispatchContainer')
        if DispatchContainer:
            is_dispatched = DispatchContainer.objects.using(using).filter(
                container_identifier=getattr(self, self.dispatched_as_container_identifier_attr()),
                is_dispatched=True,
                return_datetime__isnull=True).exists()
        return is_dispatched

    def is_dispatched_item_within_container(self, using=None):
        """Returns True if the model class is dispatched within a dispatch container.

        For example::
            a subject_consent would be considered dispatched if the method on subject_consent,
            :func:`dispatch_item_container_reference`, returned a lookup query string that points the subject consent to
            an instance of household that is itself dispatched. The household is the container. The subject consent is
            considered dispatched because it's container is dispatched. The subject consent might not have a
            corresponding DispatchItem."""
        is_dispatched = False
        dispatch_container_model_cls, lookup_attrs = self.dispatch_item_container_reference()
        if isinstance(dispatch_container_model_cls, (list, tuple)):
            dispatch_container_model_cls = get_model(dispatch_container_model_cls[0], dispatch_container_model_cls[1])
        if not isinstance(lookup_attrs, basestring):
            raise TypeError('Method dispatch_item_container_reference must return a (model class/tuple, list)')
        lookup_attrs = lookup_attrs.split('__')
        # last item in the list must be the container identifier
        if not lookup_attrs[-1:] == [dispatch_container_model_cls().dispatched_as_container_identifier_attr()]:
            raise ImproperlyConfigured('Expect last list item to be {0}. Got {1}. Model method dispatch_item_container_reference() '
                                       'must return a lookup attr string that ends in the container '
                                       'identifier field name.'.format(dispatch_container_model_cls().dispatched_as_container_identifier_attr(), lookup_attrs[-1:]))
        lookup_attrs = list(set(lookup_attrs))
        lookup_value = self
        for attrname in lookup_attrs:
            lookup_value = getattr(lookup_value, attrname)
        container_attr = dispatch_container_model_cls().dispatched_as_container_identifier_attr()
        options = {container_attr: lookup_value}
        if dispatch_container_model_cls.objects.using(using).filter(**options).exists():
            is_dispatched = dispatch_container_model_cls.objects.using(using).get(**options).is_dispatched
        return is_dispatched

    def dispatch_item_container_reference(self):
        """Returns a tuple of (model_cls, attname)  to get the model instance used as a dispatch container.

        User must override.

        ..note:: self must have a foreign key path to its container.

        (app_label, model_name), dispatch container fieldattr, qstring to dispatch container.)"""
        raise ImproperlyConfigured('Method must be overridden on model {0}'.format(self._meta.object_name))

    def is_dispatched_as_item(self, using=None):
        """Returns the models 'dispatched' status in model DispatchItem."""
        is_dispatched = False
        if self.is_dispatchable_model():
            if self.id:
                if self.get_dispatched_item(using):
                    is_dispatched = True
            if not self.is_dispatch_container_model():
                if not is_dispatched:
                    is_dispatched = self.is_dispatched_item_within_container(using)
                    if not isinstance(is_dispatched, bool):
                        raise TypeError('Expected a boolean as a return value from method is_dispatched_item_within_container(). Got {0}'.format(is_dispatched))
        return is_dispatched

    def get_dispatched_item(self, using=None):
        dispatch_item = None
        if self.id:
            if self.is_dispatchable_model():
                DispatchItem = get_model('bhp_dispatch', 'DispatchItem')
                if DispatchItem:
                    if DispatchItem.objects.using(using).filter(
                            item_app_label=self._meta.app_label,
                            item_model_name=self._meta.object_name,
                            item_pk=self.pk,
                            is_dispatched=True).exists():
                        dispatch_item = DispatchItem.objects.using(using).get(
                            item_app_label=self._meta.app_label,
                            item_model_name=self._meta.object_name,
                            item_pk=self.pk,
                            is_dispatched=True)
        return dispatch_item

    def save(self, *args, **kwargs):
        using = kwargs.get('using', None)
        if self.id:
            if self.is_dispatchable_model():
                if self.is_dispatch_container_model():
                    if self._is_dispatched_as_container(using):
                        raise AlreadyDispatchedContainer('Model {0}-{1} is currently dispatched as a container for other dispatched items.'.format(self._meta.object_name, self.pk))
                if self.is_dispatched_as_item(using):
                    raise AlreadyDispatchedItem('Model {0}-{1} is currently dispatched'.format(self._meta.object_name, self.pk))
        super(BaseDispatchSyncUuidModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
