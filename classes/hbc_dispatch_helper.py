from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import get_model, ForeignKey
from bhp_visit_tracking.models import BaseVisitTracking
from bhp_registration.models import RegisteredSubject
from bhp_dispatch.classes import DispatchController
from mochudi_survey.models import Survey


class HBCDispatchHelper(DispatchController):

    def __init__(self, debug=False, producer=None, site_code=None):
        super(HBCDispatchHelper, self).__init__(debug, producer, site_code)
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
                self.export_as_json(subject_visit.appointment, self.get_producer(), app_name=app_name)
            self.export_as_json(subject_visits, self.get_producer(), app_name=app_name)
            # fetch all scheduled_models for the visits and export
            for model_cls in scheduled_models:
                scheduled_model_instances = model_cls.objects.filter(subject_visit__in=subject_visits)
                self.export_as_json(scheduled_model_instances, self.get_producer(), app_name=app_name)

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
            self.export_as_json(membership_instances, self.get_producer())

    def import_current_survey(self):
        """Imports the current survey instance on the producer."""
        surveys = Survey.objects.filter(
                datetime_start__lte=datetime.today(),
                datetime_end__gte=datetime.today()
                )

        self.survey = surveys[0]
        if self.survey:
            self.export_as_json(self.survey, self.get_producer())

    def checkout(self, household_identifier, producer):
        """Checkout a household with the given identifier to the specified producer.

        1. Find the household, import as a json object, and save it on the producer
        2. Get the Household Structure for the household, and survey.
        3. Import the structure as a json object save it on the producer
        4. Get all household structure members with the HouseholdStructure and survey
        5. For each member:
                Fetch registered subject and save on producer
        """
        if producer:
            self.set_producer(producer)
        if self.debug:
            print "Fetching data for {0}".format(household_identifier)
        #Fetch current survey. May be this can be sent as a parameter
        if not self.survey:
            self.import_current_survey()

        if not self.survey:
            raise ValueError("No survey was specified! I'm killing myself")
        try:
            h_model = get_model('mochudi_household', 'Household')
            household = h_model.objects.get(
                household_identifier=household_identifier
                )
            self.export_as_json(household, self.get_producer())
            hs_model = get_model('mochudi_household', 'HouseholdStructure')
            if hs_model.objects.filter(household=household, survey=self.survey).exists():
                household_structure = hs_model.objects.get(
                    household=household, survey=self.survey
                    )
                self.export_as_json(household_structure, self.get_producer())
                hsm_model = get_model('mochudi_household', 'HouseholdStructureMember')
                for member in hsm_model.objects.filter(household_structure=household_structure, survey=self.survey):
                    try:
                        registered_subject = RegisteredSubject.objects.get(
                            registration_identifier=member.internal_identifier
                            )
                        self.export_as_json(registered_subject, self.get_producer())
    #                    household_survey = HouseholdSurvey.objects.using("server").get(pk=member.household_survey.pk)
    #                    self.export_as_json(household_survey, self.get_producer())
                    except ObjectDoesNotExist:
                        if self.debug:
                            print "householdstructuremember {0} has no associated registered subject".format(member.pk)
                        raise
                    self.export_as_json(member, self.get_producer())
                    self.checkout_scheduled_instances(member, self.survey, 'mochudi_subject')
                    self.checkout_membership_forms(member, self.survey)
        except ObjectDoesNotExist:
                raise
        except:
            raise

        if self.debug:
            print "Done!"
