from datetime import datetime
from django.db.models import ForeignKey
from bhp_visit_tracking.models import BaseVisitTracking
from bhp_dispatch.classes import DispatchController
from mochudi_survey.models import Survey


class DispatchHelper(DispatchController):

    def __init__(self, debug=False, producer=None, site_code=None):
        super(DispatchHelper, self).__init__(debug, producer, site_code)
        self.survey = None
        self.visit_models = {}

    def _set_visit_model_cls(self, app_name, model_cls):
        if not model_cls:
            raise TypeError('Parameter model_cls cannot be None.')

        for field in model_cls._meta.fields:
            if isinstance(field, ForeignKey):
                field_cls = field.rel.to
                if issubclass(field_cls, BaseVisitTracking):
                    self.visit_models.update({app_name: (field.name, field_cls)})

    def checkout_scheduled_instances(self, member, survey, app_name):
        """Sends scheduled instances to the producer for the given an instance of
        HouseholdStructureMember and instance of Survey.

        .. note::
           By subject visit forms, we are referring to forms that have
           reference to SubjectVisit.
        """
        print('********** CHECKING OUT SCHEDULED INSTANCES')

        scheduled_model_instances = None
        # Get all the models with reference to SubjectVisit
        scheduled_models = self._get_scheduled_models(app_name)
        # Fetch the SubjectVisit model
        visit_model_cls = self.visit_models.get(app_name)[self.VISIT_MODEL_CLS]
        # Fetch all all subject visits for the member and survey
        subject_visits = visit_model_cls.objects.filter(
            household_structure_member=member,
            survey=survey)
        if subject_visits:
            for subject_visit in subject_visits:
                # export all appointments for this subject
                self.dispatch_as_json(subject_visit.appointment, self.get_producer(), app_name=app_name)
            self.dispatch_as_json(subject_visits, self.get_producer(), app_name=app_name)
            # fetch all scheduled_models for the visits and export
            for model_cls in scheduled_models:
                scheduled_model_instances = model_cls.objects.filter(subject_visit__in=subject_visits)
                self.dispatch_as_json(scheduled_model_instances, self.get_producer(), app_name=app_name)

    def checkout_membership_forms(self, member, survey):
        """Sends membership forms to the producer for the given instance of
        HouseholdStructureMember and instance of Survey.

        .. note::
           By membership forms, we are referring to forms that have
           reference to HouseholdStructureMember. These include the
           subject visit form which we consider to be a visit form
           as is has reference to SubjectVisit.
        """
        print('********** CHECKING OUT MEMBERSHIP FORMS')

        # Fetch all the models with reference to HouseholdStructureMember
        membership_form_models = self.get_membership_form_models()
        for membership_form_model in membership_form_models:
            # If the model has reference to survey, find all instances for the
            # member and survey year else just filter on member
            if "survey" in dir(membership_form_model):
                membership_instances = membership_form_model.objects.filter(
                    registered_subject=member.registered_subject,
                    survey=survey)
            else:
                membership_instances = membership_form_model.objects.filter(
                        household_structure_member=member)
            self.dispatch_as_json(membership_instances, self.get_producer())

    def import_current_survey(self):
        """Imports the current survey instance on the producer."""
        surveys = Survey.objects.filter(
                datetime_start__lte=datetime.today(),
                datetime_end__gte=datetime.today()
                )

        self.survey = surveys[0]
        if self.survey:
            self.dispatch_as_json(self.survey, self.get_producer())

    def dispatch_prep(self, using_source, item_identifier, producer):
        return None

    def checkout(self, using_source, item_identifier, producer):
        if producer:
            self.set_producer(producer)

        if self.debug:
            print "Fetching data for {0}".format(item_identifier)

        self.dispatch_prep(using_source, item_identifier, producer)

    def dispatch_action(self, modeladmin, request, queryset, **kwargs):
        """ModelAdmin action method to dispatch all selected households to specified netbooks.

        Acts on the Algorithm:
            for each Dispatch instance:
                get a list of household identifiers
                    foreach household identifier
                        create a DispatchItem
                        set the item as Dispatch
                        set the checkout time to now
                        invoke controller.checkout (...) checkout the data to the netbook
                update Dispatch instance as checked out"""
        if len(queryset):
            helper = DispatchHelper(True)
        else:
            pass
        for qs in queryset:
            # Make sure the checkout instance is not already checked out and has not been checked back again
            if qs.is_checked_out == True and qs.is_checked_in == False:
                raise ValueError("There are households already checked to {0} that have not been checked back in!".format(qs.producer.name))
            else:
                # item identifiers are separated by new lines, so explode them on "\n"
                item_identifiers = qs.checkout_items.split()
                for item_identifier in item_identifiers:
                    # Save to producer
                    helper.checkout(item_identifier, qs.producer.name)
                    # create dispatch item
                    DispatchItem.objects.create(
                        producer=qs.producer,
                        hbc_dispatch=qs,
                        item_identifier=item_identifier,
                        is_checked_out=True,
                        datetime_checked_out=datetime.today())
                    modeladmin.message_user(
                        request, 'Checkout {0} to {1}.'.format(item_identifier, qs.producer))
                qs.datetime_checked_out = datetime.today()
                qs.is_checked_out = True
                qs.save()
                modeladmin.message_user(request, 'The selected items were successfully checkout to \'{0}\'.'.format(qs.producer))
