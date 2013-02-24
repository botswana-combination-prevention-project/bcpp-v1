import logging
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_model
from bhp_sync.models import BaseSyncUuidModel
from bhp_dispatch.exceptions import AlreadyDispatched
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
        if self.id:
            if self.is_dispatchable_model():
                if self.is_dispatched_to_producer():
                    return True
        return False

    def dispatched_as_container_identifier_attr(self):
        """Override to return the field attrname of the identifier used for the dispatch container."""
        raise ImproperlyConfigured('Method must be overridden on model {0}'.format(self._meta.object_name))

    def _is_dispatched_to_producer_as_container(self):
        is_dispatched = False
        DispatchContainer = get_model('bhp_dispatch', 'DispatchContainer')
        if DispatchContainer:
            is_dispatched = DispatchContainer.objects.filter(
                container_identifier=getattr(self, self.dispatched_as_container_identifier_attr()),
                is_dispatched=True,
                return_datetime__isnull=True).exists()
        return is_dispatched

    def is_dispatched_to_producer(self):
        """Returns lock status as a boolean needed when using this model with bhp_dispatch."""
        is_dispatched = False
        if self.id:
            DispatchItem = get_model('bhp_dispatch', 'DispatchItem')
            if DispatchItem:
                is_dispatched = DispatchItem.objects.filter(
                    item_app_label=self._meta.app_label,
                    item_model_name=self._meta.object_name,
                    item_pk=self.pk,
                    is_dispatched=True).exists()
        return is_dispatched

    def get_dispatched_item(self):
        retval = None
        if self.id:
            if self.is_dispatched:
                retval = DispatchItem.objects.get(
                            item_app_label=self._meta.app_label,
                            item_model_name=self._meta.object_name,
                            item_pk=self.pk,
                            is_dispatched=True)
        return retval

    def save(self, *args, **kwargs):
        if self.id:
            if self.is_dispatchable_model():
                if self.is_dispatch_container_model():
                    if self._is_dispatched_to_producer_as_container():
                        raise AlreadyDispatched('Model {0}-{1} is currently dispatched as a container for other dispatched items.'.format(self._meta.object_name, self.pk))
                if self.is_dispatched_to_producer():
                    raise AlreadyDispatched('Model {0}-{1} is currently dispatched'.format(self._meta.object_name, self.pk))
        super(BaseDispatchSyncUuidModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
