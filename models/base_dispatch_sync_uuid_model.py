import logging
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_model
from bhp_sync.models import BaseSyncUuidModel
from bhp_dispatch.exceptions import AlreadyDispatchedContainer, AlreadyDispatchedItem
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
                if self.is_dispatched_as_item():
                    return True
        return False

    def dispatched_as_container_identifier_attr(self):
        """Override to return the field attrname of the identifier used for the dispatch container."""
        raise ImproperlyConfigured('Method must be overridden on model {0}'.format(self._meta.object_name))

    def _is_dispatched_as_container(self, using=None):
        if not using:
            using = 'default'
        is_dispatched = False
        DispatchContainer = get_model('bhp_dispatch', 'DispatchContainer')
        if DispatchContainer:
            is_dispatched = DispatchContainer.objects.using(using).filter(
                container_identifier=getattr(self, self.dispatched_as_container_identifier_attr()),
                is_dispatched=True,
                return_datetime__isnull=True).exists()
        return is_dispatched

    def is_dispatched_as_item(self, using=None):
        """Returns the models 'dispatched' status in model DispatchItem."""
        if not using:
            using = 'default'
        is_dispatched = False
        if self.id:
            if self.is_dispatchable_model():
                DispatchItem = get_model('bhp_dispatch', 'DispatchItem')
                if DispatchItem:
                    is_dispatched = DispatchItem.objects.using(using).filter(
                        item_app_label=self._meta.app_label,
                        item_model_name=self._meta.object_name,
                        item_pk=self.pk,
                        is_dispatched=True).exists()
        return is_dispatched

    def get_dispatched_item(self, using=None):
        if not using:
            using = 'default'
        dispatch_item = None
        if self.id:
            if self.is_dispatched:
                DispatchItem = get_model('bhp_dispatch', 'DispatchItem')
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
