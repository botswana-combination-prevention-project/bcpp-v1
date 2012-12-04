import logging
from datetime import datetime
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
        self._dispatch = None
        self.set_dispatch()

    def set_dispatch(self):
        """Creates a dispatch instance for this controller sessions."""
        Dispatch = get_model('bhp_dispatch', 'Dispatch')
        self._dispatch = Dispatch.objects.create(producer=self.get_producer())

    def get_dispatch(self):
        """Gets the dispatch instance for this controller sessions."""
        if not self._dispatch:
            self.set_dispatch()
        return self._dispatch

    def set_visit_model_fkey(self, model_cls, visit_model_cls):
        for fld in model_cls.objects._meta.fields:
            if isinstance(fld, (ForeignKey, OneToOneField)):
                if isinstance(fld.rel.to, visit_model_cls):
                    self._visit_model_fkey_name = fld.name

    def get_visit_model_fkey(self, app_name, model_cls, visit_model_cls=None):
        if not self._visit_model_fkey_name:
            self.set_visit_model_fkey(model_cls, visit_model_cls)
        return self._visit_model_fkey_name

    def dispatch_appointments(self, registered_subject):
        """Dispatches all apoointments for this registered subject."""
        Appointments = get_model('bhp_appointment', 'Appointment')
        self.dispatch_as_json(Appointments.objects.filter(registered_subject=registered_subject))

    def dispatch_scheduled_instances(self, app_name, registered_subject, **kwargs):
        """Sends scheduled instances to the producer for the given an instance of registered_subject.

        Keywords:
            kwargs must be field_attr: value pairs to pass directly to the visit model. Any django syntax will work.

        .. note::
           By scheduled_instances, we are referring to models that have a foreign key to a subclass
           of :mod:`bhp_visit_tracking`'s :class:`BaseVisitTracking` base model.
           For example, to maternal_visit, infant_visit, subject_visit, patient_visit, etc
        """
        self.dispatch_appointments(registered_subject)
        # Get all the models with reference to SubjectVisit
        scheduled_models = self.get_scheduled_models(app_name)
        # get the visit model class for this app
        visit_model_cls = self.get_visit_model_cls(app_name, index='cls')
        # Fetch all all subject visits for the member and survey
        visits = visit_model_cls.objects.filter(appointment__registered_subject=registered_subject, **kwargs)
        visit_fld_name = None
        if visits:
            for visit in visits:
                # export all appointments for this visit
                self.dispatch_as_json(visit.appointment, app_name=app_name)
            self.dispatch_as_json(visits, app_name=app_name)
            # fetch all scheduled_models for the visits and export
            for model_cls in scheduled_models:
                if not visit_fld_name:
                    for fld in model_cls._meta.fields:
                        if isinstance(fld, (ForeignKey, OneToOneField)):
                            if issubclass(fld.rel.to, visit_model_cls):
                                visit_fld_name = fld.name
                scheduled_instances = model_cls.objects.filter(**{'{0}__in'.format(visit_fld_name): visits})
                self.dispatch_as_json(scheduled_instances, app_name=app_name)

    def dispatch_membership_forms(self, registered_subject, **kwargs):
        """Gets all instances of visible membership forms for this registered_subject and dispatches.

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
            self.dispatch_as_json(instances)

    def dispatch_prep(self, item_identifier):
        """Returns a registered_subject instance (or None) after processing.

        This is the main data query for dispatching and is to be overriden by the user
        to access local app models."""
        registered_subject = None
        options = {}  # extra options for database query
        return registered_subject, options

    def dispatch(self, item_identifier):
        """Dispatches items to a device calling the user overridden :func:`dispatch_prep`."""
        # check source for the producer based on using_destination.
        if self.debug:
            logger.info("Dispatching items for {0}".format(item_identifier))
        # is this item already dispatched?
        created, dispatch_item = None, None
        if not self.is_dispatched(item_identifier):
            registered_subjects = self.dispatch_prep(item_identifier)
            #if registered_subjects:
            #    for registered_subject in registered_subjects:
            #        self.dispatch_membership_forms(registered_subject)
            created, dispatch_item = self.create_dispatch_item_instance(item_identifier, registered_subjects=registered_subjects)
        return dispatch_item

    def is_dispatched(self, item_identifier):
        """Checks if a dispatch item is dispatched.

        .. note:: to block saving a dispatched instance, see the signals."""
        DispatchItem = get_model('bhp_dispatch', 'DispatchItem')
        if DispatchItem.objects.using(self.get_using_source()).filter(
                item_identifier=item_identifier,
                is_dispatched=True).exists():
            return True
        return False

    def create_dispatch_item_instance(self, item_identifier, **kwargs):
        """Creates a dispatch item instance for given dispatch instance and item_identifier."""
        # TODO: may want this to be get_or_create so dispatch item instances are re-used.
        DispatchItem = get_model('bhp_dispatch', 'DispatchItem')
        created = True
        dispatch_item = DispatchItem.objects.create(
            producer=self.get_producer(),
            dispatch=self.get_dispatch(),
            item_identifier=item_identifier,
            is_dispatched=True,
            dispatch_datetime=datetime.today())
        return created, dispatch_item

    def dispatch_from_view(self, queryset, **kwargs):
        """Confirms no items in queryset are dispatched then tries to dispatch each one."""
        any_dispatched = False  # are any items dispatched already?
        any_transactions = True
        if not self.has_outgoing_transactions():
            any_transactions = False
            for qs in queryset:
                item_identifier = getattr(qs, self.dispatch_model_item_identifier_field)
                if self.is_dispatched(item_identifier):
                    any_dispatched = True
                    break
            if not any_dispatched:
                for qs in queryset:
                    item_identifier = getattr(qs, self.dispatch_model_item_identifier_field)
                    self.dispatch(item_identifier)
                logger.info("Updating the Crypt table...")
                self.update_model(('bhp_crypto', 'crypt'))
        return any_dispatched, any_transactions
