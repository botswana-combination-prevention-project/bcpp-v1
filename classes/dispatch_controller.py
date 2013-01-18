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

    def __init__(self, using_source, using_destination, app_name, model_name, identifier_field_name, dispatch_url, **kwargs):
        super(DispatchController, self).__init__(using_source, using_destination, **kwargs)
        self._dispatch_app_name = None
        self._dispatch_model_name = None
        self._visit_models = {}
        self._dispatch = None
        self._dispatch_url = None
        self._dispatch_admin_url = None
        self._dispatch_model = None
        self._dispatch_model_item_identifier_field = None
        self._dispatch_admin_url = None
        self.set_dispatch_app_name(app_name)
        self.set_dispatch_model_name(model_name)
        self.set_dispatch_model_item_identifier_field(identifier_field_name)
        self.set_dispatch_url(dispatch_url)
        self.set_dispatch_instance()

    def set_dispatch_app_name(self, value):
        if not value:
            raise AttributeError('The app_name of the dispatch model cannot be None. Set this in __init__() of the subclass.')
        self._dispatch_app_name = value

    def get_dispatch_app_name(self):
        """Gets the app_name for the dispatching model."""
        if not self._dispatch_app_name:
            self.set_dispatch_app_name()
        return self._dispatch_app_name

    def set_dispatch_model_name(self, value):
        if not value:
            raise AttributeError('The model_name of the dispatch model cannot be None. Set this in __init__() of the subclass.')
        self._dispatch_model_name = value

    def get_dispatch_model_name(self):
        """Gets the model name for the dispatching model."""
        if not self._dispatch_model_name:
            self.set_dispatch_model_name()
        return self._dispatch_model_name

    def set_dispatch_model_item_identifier_field(self, value=None):
        """Sets identifier field attribute of the dispatch model."""
        if not value:
            raise AttributeError('The identifier field of the dispatch model cannot be None. Set this in __init__() of the subclass.')
        self._dispatch_model_item_identifier_field = value

    def get_dispatch_model_item_identifier_field(self):
        """Gets the model name for the dispatching model."""
        if not self._dispatch_model_item_identifier_field:
            self.set_dispatch_model_item_identifier_field()
        return self._dispatch_model_item_identifier_field

    def set_dispatch_model(self):
        """Sets the model class for the dispatching model."""
        self._dispatch_model = get_model(self.get_dispatch_app_name(), self.get_dispatch_model_name())
        self.set_dispatch_modeladmin_url()

    def get_dispatch_model(self):
        """Gets the model class for the dispatching model."""
        if not self._dispatch_model:
            self.set_dispatch_model()
        return self._dispatch_model

    def set_dispatch_modeladmin_url(self):
        """Sets the modeladmin url for the dispatching model."""
        self._dispatch_modeladmin_url = '/admin/{0}/{1}/'.format(self.get_dispatch_app_name(), self.get_dispatch_model_name())

    def get_dispatch_modeladmin_url(self):
        """Gets the modeladmin url for the dispatching model."""
        if not self._dispatch_modeladmin_url:
            self.set_dispatch_modeladmin_url()
        return self._dispatch_modeladmin_url

    def set_dispatch_url(self, value=None):
        if not value:
            raise AttributeError('Dispatch url cannot be None. Set this in __init__() of the subclass.')
        self._dispatch_url = value

    def get_dispatch_url(self):
        if not self._dispatch_url:
            self.set_dispatch_url()
        return self._dispatch_url

    def set_dispatch_instance(self):
        """Creates a dispatch instance for this controller sessions."""
        Dispatch = get_model('bhp_dispatch', 'Dispatch')
        self._dispatch = Dispatch.objects.create(producer=self.get_producer())

    def get_dispatch_instance(self):
        """Gets the dispatch instance for this controller sessions."""
        if not self._dispatch:
            self.set_dispatch_instance()
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
        """Dispatches all appointments for this registered subject."""
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
        scheduled_models = self.get_scheduled_models()
        # get the visit model class for this app
        #for app_name, scheduled_model_classes in scheduled_models.iteritems():
        for scheduled_model_class in scheduled_models:
            visit_model_cls = self.get_visit_model_cls(app_name, scheduled_model_class, index='cls')
            # Fetch all all subject visits for the member and survey
            visits = visit_model_cls.objects.filter(appointment__registered_subject=registered_subject, **kwargs)
            visit_fld_name = None
            if visits:
                for visit in visits:
                    # export all appointments for this visit
                    #self.dispatch_as_json(visit.appointment, app_name=app_name)
                    self.dispatch_as_json(visit, app_name=app_name)
                    self.dispatch_labs_requisitions(visit, registered_subject)
            # fetch all scheduled_models for the visits and export
            #for model_cls in scheduled_model_class:
                #if not visit_fld_name:
                for fld in scheduled_model_class._meta.fields:
                    if isinstance(fld, (ForeignKey, OneToOneField)):
                        if issubclass(fld.rel.to, visit_model_cls):
                            visit_fld_name = fld.name
                scheduled_instances = scheduled_model_class.objects.filter(**{'{0}__in'.format(visit_fld_name): visits})
                self.dispatch_as_json(scheduled_instances, app_name=app_name)
    
    def dispatch_labs_requisitions(self, subject_visit, registered_subject):
        """Dispatches all lab requisitions for this subject visit."""
        Lab_requisitions = get_model('mochudi_survey_lab', 'SubjectRequisition')
        self.dispatch_as_json(Lab_requisitions.objects.filter(subject_visit=subject_visit.pk))
        
        Receive = get_model('lab_clinic_api', 'Receive')
        receives_list = Receive.objects.filter(registered_subject=registered_subject)
        self.dispatch_as_json(receives_list)
        
        Aliquot = get_model('lab_clinic_api', 'Aliquot')
        aliquot_list = Aliquot.objects.filter(receive__in=receives_list)
        self.dispatch_as_json(aliquot_list)
        
        Order = get_model('lab_clinic_api', 'Order')
        order_list = Order.objects.filter(aliquot__in=aliquot_list)
        self.dispatch_as_json(order_list)
        
        Result = get_model('lab_clinic_api', 'Result')
        result_list = Result.objects.filter(order__in=order_list)
        self.dispatch_as_json(result_list)
        
        ResultItem = get_model('lab_clinic_api', 'ResultItem')
        result_item_list = ResultItem.objects.filter(result__in=order_list)
        self.dispatch_as_json(result_item_list)
        
        AdditionalLabEntryBucket = get_model('bhp_lab_entry', 'AdditionalLabEntryBucket')
        self.dispatch_as_json(AdditionalLabEntryBucket.objects.filter(registered_subject=registered_subject.pk))
        ScheduledLabEntryBucket = get_model('bhp_lab_entry', 'ScheduledLabEntryBucket')
        self.dispatch_as_json(ScheduledLabEntryBucket.objects.filter(registered_subject=registered_subject.pk))
    
    def dispatch_membership_forms(self, registered_subject, **kwargs):
        """Gets all instances of visible membership forms for this registered_subject and dispatches.

        Keywords:
            kwargs: must be field_attr: value pairs to pass directly to the visit model. Any django syntax will work.

        .. seealso::
            See app :mod:`bhp_visit` for an explanation of membership forms.
        """
        for membershipform_model in self.get_membershipform_models():
            try:
                if membershipform_model:
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
        """Creates a dispatch item instance for given dispatch instance and item_identifier

        .. note:: Uses the pk instead of subject_identifier as subject_identifier may be None."""
        # TODO: may want this to be get_or_create so dispatch item instances are re-used.
        DispatchItem = get_model('bhp_dispatch', 'DispatchItem')
        created = True
        registered_subjects = kwargs.get('registered_subjects', [])
        pk_list = [rs.pk for rs in registered_subjects]
        dispatch_item = DispatchItem.objects.create(
            producer=self.get_producer(),
            dispatch=self.get_dispatch_instance(),
            item_identifier=item_identifier,
            subject_identifiers=' '.join(pk_list),
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
                item_identifier = getattr(qs, self.get_dispatch_model_item_identifier_field())
                if self.is_dispatched(item_identifier):
                    any_dispatched = True
                    break
            if not any_dispatched:
                for qs in queryset:
                    item_identifier = getattr(qs, self.get_dispatch_model_item_identifier_field())
                    self.dispatch(item_identifier)
                self.dispatch_crypt()
        return any_dispatched, any_transactions

    def dispatch_crypt(self):
        logger.info("Updating the Crypt table...")
        self.update_model(('bhp_crypto', 'crypt'))
