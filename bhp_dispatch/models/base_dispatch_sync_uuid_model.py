import logging
import copy
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_model
from bhp_sync.models import BaseSyncUuidModel
from bhp_dispatch.exceptions import AlreadyDispatchedContainer, AlreadyDispatchedItem, DispatchContainerError
#from bhp_dispatch.models import DispatchItemRegister, DispatchContainerRegister


logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class BaseDispatchSyncUuidModel(BaseSyncUuidModel):

    """Base model for all UUID models and adds dispatch methods and signals. """

    def is_dispatch_container_model(self):
        """Flags a model as a container model that if dispatched will not appear in DispatchItems, but rather in DispatchContainerRegister."""
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

    def dispatched_as_container_identifier_attr(self):
        """Override to return the field attrname of the identifier used for the dispatch container.

        Must be an field attname on the model used as a dispatch container, such as, household_identifier on model Household."""
        raise ImproperlyConfigured('Model {0} is not configured for dispatch as a container. Missing method dispatched_as_container_identifier_attr()'.format(self._meta.object_name))

    def is_dispatched_as_container(self, using=None):
        """Determines if a model instance is dispatched as a container.

        For example: a household model instance may serve as a container for all household members and data."""
        is_dispatched = False
        if self.is_dispatch_container_model():
            DispatchContainerRegister = get_model('bhp_dispatch', 'DispatchContainerRegister')
            if DispatchContainerRegister:
                is_dispatched = DispatchContainerRegister.objects.using(using).filter(
                    container_identifier=getattr(self, self.dispatched_as_container_identifier_attr()),
                    is_dispatched=True,
                    return_datetime__isnull=True).exists()
        return is_dispatched

    def is_dispatched_within_user_container(self, using=None):
        """Returns True if the model class is dispatched within a user container.

        ..note:: an item is considered dispatched if it's container is dispatched. It usually
                 is also registered as a dispatched item, but as described below, this may
                 not always be true.

        For example::
            a subject_consent would be considered dispatched if the method on subject_consent,
            :func:`dispatch_container_lookup`, returned a lookup query string that points the subject consent to
            an instance of household that is itself dispatched. The household is the container. The subject consent is
            considered dispatched because it's container is dispatched. The subject consent might not have a
            corresponding DispatchItemRegister. This might happen if the subject_consent is created on the producer and re-synced
            with the source before the Household is returned."""
        is_dispatched = False
        if self.dispatch_container_lookup():
            user_container_model_cls, lookup_attrs = self.dispatch_container_lookup()
            if isinstance(user_container_model_cls, (list, tuple)):
                user_container_model_cls = get_model(user_container_model_cls[0], user_container_model_cls[1])
            if not isinstance(lookup_attrs, basestring):
                raise TypeError('Method dispatch_container_lookup must return a (model class/tuple, list) that points to the user container')
            lookup_attrs = lookup_attrs.split('__')
            # last item in the list must be the container identifier
#            if not lookup_attrs[-1:] == [user_container_model_cls().dispatched_as_container_identifier_attr()]:
#                raise ImproperlyConfigured('Expect last list item to be {0}. Got {1}. Model method dispatch_container_lookup() '
#                                           'must return a lookup attr string that ends in the container '
#                                           'identifier field name.'.format(user_container_model_cls().dispatched_as_container_identifier_attr(), lookup_attrs[-1:]))

            lookup_value = self  # why is this set to self?

            # FIXME: if lookup value gets set to None below (e.g. attribute Plot is None and the user container is Plot)
            #        that means the user_container value is not known and is_dispatched will be false.
            #        this condition should not occur!

            for attrname in lookup_attrs:
                lookup_value = getattr(lookup_value, attrname, None)  # is this supposed to default to self?
            if not lookup_value:
                raise DispatchContainerError('Expected to get a value for the user_container model \'{0}\' on dispatch_container_lookup for model \'{1}\'.'.format(user_container_model_cls, self.__class__))
            container_attr = user_container_model_cls().dispatched_as_container_identifier_attr()
            options = {container_attr: lookup_value}
            if user_container_model_cls.objects.using(using).filter(**options).exists():
                # found user container instance, is it dispatched?
                is_dispatched = user_container_model_cls.objects.using(using).get(**options).is_dispatched_as_container(using)
        return is_dispatched

    def dispatch_container_lookup(self):
        """Returns a query string in the django format.

        User must override.

        if the model has no path to the user_container, such as Appointment or RegisteredSubject, override like this::

            def dispatch_container_lookup(self):
                return None
        if the model does have a relational path to the user_container, override like this::

            def dispatch_container_lookup(self):
                return 'django__style__path__to__container'

        For example:
            with a relational structure like this::
                self
                    household_structure_member
                        household_structure
                            household.household_identifier

            where 'household' is the user container with identifier attr 'household_identifier',
            <self> would return something like this:
                'household_structure_member__household_structure__household__household_identifier'
        """
        raise ImproperlyConfigured('Model {0} is not configured for dispatch. Missing method \'dispatch_container_lookup\''.format(self._meta.object_name))

    def _bypass_for_edit(self):
        if self.bypass_for_edit_dispatched_as_item():
            if not self.id:
                raise AlreadyDispatchedItem('Model {0}-{1}, although dispatched, may only be conditionally edited. New instances are not allowed.'.format(self._meta.object_name, self.pk))
            return True
        return False

    def bypass_for_edit_dispatched_as_item(self):
        """Users may override to allow a model to be edited even thoug it is dispatched.

        .. warning:: avoid using this. it only allows edits. you are responsible to
                  ensure your actions will not lead to data conflicts. so it is best to also
                  limit which fields may be edited.
        """
        return False

    def is_dispatched_as_item(self, using=None, user_container=None):
        """Returns the models 'dispatched' status in model DispatchItemRegister."""
        is_dispatched = False
        if self.is_dispatchable_model():
            if not self._bypass_for_edit():
                if self.id:
                    if self.get_dispatched_item(using):
                        is_dispatched = True
                if not is_dispatched:
                    if not self.is_dispatch_container_model():
                        # if item is not registered with DispatchItemRegister AND we are not checking on behalf of
                        # a user_container ...
                        if not is_dispatched and not user_container:
                            is_dispatched = self.is_dispatched_within_user_container(using)
                            if not isinstance(is_dispatched, bool):
                                raise TypeError('Expected a boolean as a return value from method is_dispatched_within_user_container(). Got {0}'.format(is_dispatched))
        return is_dispatched

    def get_dispatched_item(self, using=None):
        dispatch_item = None
        if self.id:
            if self.is_dispatchable_model():
                DispatchItemRegister = get_model('bhp_dispatch', 'DispatchItemRegister')
                if DispatchItemRegister:
                    if DispatchItemRegister.objects.using(using).filter(
                            item_app_label=self._meta.app_label,
                            item_model_name=self._meta.object_name,
                            item_pk=self.pk,
                            is_dispatched=True).exists():
                        dispatch_item = DispatchItemRegister.objects.using(using).get(
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
                    if self.is_dispatched_as_container(using):
                        raise AlreadyDispatchedContainer('Model {0}-{1} is currently dispatched as a container for other dispatched items.'.format(self._meta.object_name, self.pk))
                if self.is_dispatched_as_item(using):
                    raise AlreadyDispatchedItem('Model {0}-{1} is currently dispatched'.format(self._meta.object_name, self.pk))
        super(BaseDispatchSyncUuidModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
