import logging
from datetime import datetime
from django.contrib import messages
from django.db.models import ForeignKey, OneToOneField, get_model
from django.core.exceptions import FieldError
from bhp_dispatch.classes import BaseDispatchController

logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class AlreadyDispatched(Exception):
    pass


class DispatchController(BaseDispatchController):

    def __init__(self, using_source, using_destination, **kwargs):
        super(DispatchController, self).__init__(using_source, using_destination, **kwargs)
        self._visit_models = {}

    def set_visit_model_fkey(self, model_cls, visit_model_cls):
        for fld in model_cls.objects._meta.fields:
            if isinstance(fld, (ForeignKey, OneToOneField)):
                if isinstance(fld.rel.to, visit_model_cls):
                    self._visit_model_fkey_name = fld.name

    def get_visit_model_fkey(self, app_name, model_cls, visit_model_cls=None):
        if not self._visit_model_fkey_name:
            self.set_visit_model_fkey(model_cls, visit_model_cls)
        return self._visit_model_fkey_name

    def dispatch_scheduled_instances(self, app_name, registered_subject, **kwargs):
        """Sends scheduled instances to the producer for the given an instance of registered_subject.

        Keywords:
            kwargs must be field_attr: value pairs to pass directly to the visit model. Any django syntax will work.

        .. note::
           By scheduled_instances, we are referring to models that have a foreign key to a subclass
           of :mod:`bhp_visit_tracking`'s :class:`BaseVisitTracking` base model.
           For example, to maternal_visit, infant_visit, subject_visit, patient_visit, etc
        """
        # Get all the models with reference to SubjectVisit
        scheduled_models = self.get_scheduled_models(app_name)
        # get the visit model class for this app
        visit_model_cls = self.get_visit_model_cls(app_name, 'cls')
        # Fetch all all subject visits for the member and survey
        visits = visit_model_cls.objects.filter(appointment__registered_subject=registered_subject, **kwargs)
        visit_fld_name = None
        if visits:
            for visit in visits:
                # export all appointments for this subject
                self.dispatch_as_json(visit.appointment, self.get_producer(), app_name=app_name)
            self.dispatch_as_json(visits, self.get_producer(), app_name=app_name)
            # fetch all scheduled_models for the visits and export
            for model_cls in scheduled_models:
                if not visit_fld_name:
                    for fld in model_cls.objects._meta.fields:
                        if isinstance(fld, (ForeignKey, OneToOneField)):
                            if isinstance(fld.rel.to, visit_model_cls):
                                visit_fld_name = fld.name
                scheduled_instances = model_cls.objects.filter(**{'{0}__in'.format(visit_fld_name): visits})
                self.dispatch_as_json(scheduled_instances, self.get_producer(), app_name=app_name)

    def dispatch_membership_forms(self, registered_subject, **kwargs):
        """Gets all instances of membership forms for this registered_subject and dispatches.

        Keywords:
            kwargs: must be field_attr: value pairs to pass directly to the visit model. Any django syntax will work.

        .. seealso::
            See app :mod:`bhp_visit` for an explanation of membership forms.
        """
        for membershipform_model in self.get_membershipform_models():
            try:
                instances = membershipform_model.objects.filter(
                    registered_subject=registered_subject,
                    **kwargs)
            except FieldError:
                instances = membershipform_model.objects.filter(registered_subject=registered_subject)
            self.dispatch_as_json(instances, self.get_producer())

    def dispatch_prep(self, item_identifier):
        """Returns a dispatch instance after dispatching.

        This is the main data query for dispatching and is to be overriden by the user
        to access local app models."""
        return None

    def dispatch(self, item_identifier):
        """Dispatches items to a device calling the user overridden :func:`dispatch_prep`."""
        # check source for the producer based on using_destination.
        if self.debug:
            logger.info("Dispatching items for {0}".format(item_identifier))
        # is this item already dispatched?
        if not self.is_dispatched(item_identifier):
            self.create_dispatch_item_instance(self.dispatch_prep(item_identifier), item_identifier)

    def is_dispatched(self, item_identifier):
        """Checks if a dispatch item is dispatched."""
        DispatchItem = get_model('bhp_dispatch', 'DispatchItem')
        if DispatchItem.objects.using(self.get_using_source()).filter(
                item_identifier=item_identifier,
                is_dispatched=True).exists():
            dispatch_item = DispatchItem.objects.using(self.get_using_source()).get(
                item_identifier=item_identifier,
                is_dispatched=True)
            raise AlreadyDispatched('Item {0} is already dispatched to producer {1}.'.format(item_identifier, dispatch_item.producer))

    def create_dispatch_item_instance(self, dispatch, item_identifier):
        """Creates a dispatch item instance for given dispatch instance and item_identifier."""
        # TODO: may want this to be get_or_create so dispatch item instances are re-used.
        DispatchItem = get_model('bhp_dispatch', 'DispatchItem')
        created = True
        dispatch_item = DispatchItem.objects.create(
            producer=self.get_producer(),
            dispatch=dispatch,
            item_identifier=item_identifier,
            is_dispatched=True,
            dispatch_datetime=datetime.today())
        return created, dispatch_item

    def dispatch_action(self, modeladmin, request, queryset, **kwargs):
        """ModelAdmin action method to dispatch all selected items to specified producer.

        Acts on the Algorithm::

            for each Dispatch instance:
                get a list of household identifiers
                    foreach household identifier
                        create a DispatchItem
                        set the item as Dispatch
                        set the checkout time to now
                        invoke controller.checkout (...) checkout the data to the netbook
                update Dispatch instance as checked out
        """
        for qs in queryset:
            # Make sure the dispatch instance is not already dispatched
            if qs.is_dispatched():
                modeladmin.message_user(request, 'Producer {0} has pending dispatched items. '
                                                 'Return these items first. Cannot '
                                                 'continue.'.format(qs.producer.name), level=messages.ERROR)
                break
            else:
                # item identifiers are separated by new lines, so explode them on "\n"
                item_identifiers = qs.dispatch_items.split()
                for item_identifier in item_identifiers:
                    # dispatch items to this producer
                    # TODO: this should be the destination and not producer instance??
                    self.dispatch(item_identifier)
                    modeladmin.message_user(
                        request, 'Dispatch {0} to {1}.'.format(item_identifier, qs.producer.name))
                qs.dispatch_datetime = datetime.today()
                qs.is_dispatched = True
                qs.save()
                modeladmin.message_user(request, 'The selected items were successfully dispatched to \'{0}\'.'.format(qs.producer.name))
