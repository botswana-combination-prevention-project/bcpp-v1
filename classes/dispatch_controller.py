import logging
from django.db.models import ForeignKey, OneToOneField, get_model
from django.core.exceptions import FieldError
from bhp_lab_tracker.models import HistoryModel
from bhp_dispatch.classes import BaseDispatchController


logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class AlreadyDispatched(Exception):
    pass


class DispatchController(BaseDispatchController):

    def __init__(self, using_source,
                 using_destination,
                 user_container_app_label,
                 user_container_model_name,
                 user_container_identifier_attrname,
                 user_container_identifier,
                 dispatch_url,
                 **kwargs):
        super(DispatchController, self).__init__(using_source,
            using_destination,
            user_container_app_label,
            user_container_model_name,
            user_container_identifier_attrname,
            user_container_identifier,
            **kwargs)
        self._dispatch_url = None
        self._set_dispatch_url(dispatch_url)

    def _dispatch_prep(self):
        """Wrapper for user method :func:`dispatch_prep`."""
        self.dispatch_prep()

    def dispatch_prep(self, item_identifier):
        """Returns a list of RegisteredSubject instances.

        This is the main data query for dispatching and is to be overriden by the user
        to access local app models."""
        registered_subjects = []
        return registered_subjects

    def dispatch(self):
        """Dispatches items to a device by creating a dispatch item instance.

        ..note:: calls the user overridden :func:`dispatch_prep`."""
        # check source for the producer based on using_destination.
        if self.debug:
            logger.info("Dispatching items for {0}".format(self.get_user_container_identifier()))
        self._dispatch_prep()

    def _set_dispatch_url(self, value=None):
        """Sets the dispatch url for the dispatching model."""
        if not value:
            raise AttributeError('Dispatch url cannot be None. Set this in __init__() of the subclass.')
        self._dispatch_url = value

    def get_dispatch_url(self):
        """Gets the dispatch url for the dispatching model."""
        if not self._dispatch_url:
            self._set_dispatch_url()
        return self._dispatch_url

    def set_visit_model_fkey(self, model_cls, visit_model_cls):
        """Subject forms will have a foreign key to a visit model instance. This sets that foreign key."""
        for fld in model_cls.objects._meta.fields:
            if isinstance(fld, (ForeignKey, OneToOneField)):
                if isinstance(fld.rel.to, visit_model_cls):
                    self._visit_model_fkey_name = fld.name

    def get_visit_model_fkey(self, app_label, model_cls, visit_model_cls=None):
        """Gets the foreign key to the subject visit model instance."""
        if not self._visit_model_fkey_name:
            self.set_visit_model_fkey(model_cls, visit_model_cls)
        return self._visit_model_fkey_name

    def dispatch_lab_tracker_history(self, registered_subject, container, group_name=None):
        """Dispatches all lab tracker history models for this subject.

        ..seealso:: module :mod:`bhp_lab_tracker`.
        """
        if registered_subject:
            if registered_subject.subject_identifier:
                options = {'subject_identifier': registered_subject.subject_identifier}
                if group_name:
                    options.update({'group_name': group_name})
                history_models = HistoryModel.objects.filter(**options)
                self.dispatch_user_items_as_json(history_models, container)

    def dispatch_appointments(self, registered_subject, container):
        """Dispatches all appointments for this registered subject.

        ..seealso:: module :mod:`bhp_appointment`
        """
        Appointments = get_model('bhp_appointment', 'Appointment')
        self.dispatch_user_items_as_json(Appointments.objects.filter(registered_subject=registered_subject), container)

    def dispatch_scheduled_instances(self, app_label, registered_subject, container, **kwargs):
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
        scheduled_models = self.get_scheduled_models()
        # get the visit model class for this app
        #for app_label, scheduled_model_classes in scheduled_models.iteritems():
        for scheduled_model_class in scheduled_models:
            visit_model_cls = self.get_visit_model_cls(app_label, scheduled_model_class, index='cls')
            # Fetch all all subject visits for the member and survey
            visits = visit_model_cls.objects.filter(appointment__registered_subject=registered_subject, **kwargs)
            visit_fld_name = None
            if visits:
                for visit in visits:
                    # export all appointments for this visit
                    #self.dispatch_user_items_as_json(visit.appointment, app_label=app_label)
                    self.dispatch_user_items_as_json(visit, container)
            # fetch all scheduled_models for the visits and export
            #for model_cls in scheduled_model_class:
                #if not visit_fld_name:
                for fld in scheduled_model_class._meta.fields:
                    if isinstance(fld, (ForeignKey, OneToOneField)):
                        if issubclass(fld.rel.to, visit_model_cls):
                            visit_fld_name = fld.name
                scheduled_instances = scheduled_model_class.objects.filter(**{'{0}__in'.format(visit_fld_name): visits})
                self.dispatch_user_items_as_json(scheduled_instances, container)

    def dispatch_labs_requisitions(self, registered_subject, container):
        """Dispatches all lab requisitions for this subject."""
        Lab_requisitions = get_model('mochudi_survey_lab', 'SubjectRequisition')
        labs = Lab_requisitions.objects.filter(
                subject_visit__household_structure_member__registered_subject=registered_subject
                )
        for lab in labs:
            if lab.subject_visit:
                self.dispatch_user_items_as_json(lab.subject_visit, container)
        self.dispatch_user_items_as_json(labs, container)
        AdditionalLabEntryBucket = get_model('bhp_lab_entry', 'AdditionalLabEntryBucket')
        self.dispatch_user_items_as_json(AdditionalLabEntryBucket.objects.filter(registered_subject=registered_subject.pk), container)
        ScheduledLabEntryBucket = get_model('bhp_lab_entry', 'ScheduledLabEntryBucket')
        self.dispatch_user_items_as_json(ScheduledLabEntryBucket.objects.filter(registered_subject=registered_subject.pk), container)

    def dispatch_membership_forms(self, registered_subject, container, **kwargs):
        """Gets all instances of visible membership forms for this registered_subject and dispatches.

        Keywords:
            kwargs: must be field_attr: value pairs to pass directly to the visit model. Any django syntax will work.

        .. seealso::
            See app :mod:`bhp_visit` for an explanation of membership forms.
        """

        membership_forms = self.get_membershipform_models()
        for membershipform_model in membership_forms:
            try:
                if membershipform_model:
                    instances = membershipform_model.objects.filter(
                        registered_subject=registered_subject,
                        **kwargs)
            except FieldError:
                instances = membershipform_model.objects.filter(registered_subject=registered_subject)
            self.dispatch_user_items_as_json(instances, container)

    def dispatch_from_view(self, queryset, **kwargs):
        """Confirms no items in queryset are dispatched then follows by trying to dispatch each one.

        Does this by checking bhp_sync.outgoing_transactions in the netbook.
        """
        any_dispatched = False  # are any items dispatched already?
        any_transactions = True
        if not self.has_outgoing_transactions():
            any_transactions = False
            for qs in queryset:
                if qs.is_dispatched:
                    any_dispatched = True
                    break
            if not any_dispatched:
                for qs in queryset:
                    self.dispatch()
                self.dispatch_crypt()
                self.dispatch_registered_subjects()
        return any_dispatched, any_transactions

    def dispatch_crypt(self):
        logger.info("Updating the Crypt table...")
        self.update_model(('bhp_crypto', 'crypt'))

    def dispatch_registered_subjects(self):
        logger.info("Updating the Registered Subjects table...")
        self.update_model(('bhp_registration', 'RegisteredSubject'))