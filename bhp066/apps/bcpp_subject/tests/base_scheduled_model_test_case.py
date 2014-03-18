from datetime import datetime

from django.test import TestCase

from edc.core.bhp_content_type_map.classes import ContentTypeMapHelper
from edc.core.bhp_content_type_map.models import ContentTypeMap
from edc.core.bhp_variables.tests.factories import StudySpecificFactory, StudySiteFactory
from edc.subject.appointment.models import Appointment
from edc.subject.appointment.tests.factories import ConfigurationFactory
from edc.subject.consent.tests.factories import ConsentCatalogueFactory
from edc.subject.entry.tests.factories import EntryFactory
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.registration.models import RegisteredSubject
from edc.subject.visit_schedule.tests.factories import MembershipFormFactory, ScheduleGroupFactory, VisitDefinitionFactory

from apps.bcpp_household.models import Plot, Household, HouseholdStructure
from apps.bcpp_household.tests.factories import PlotFactory
from apps.bcpp_household_member.tests.factories import HouseholdMemberFactory
from apps.bcpp_subject.tests.factories import SubjectConsentFactory, SubjectVisitFactory
from apps.bcpp_survey.tests.factories import SurveyFactory


class BaseScheduledModelTestCase(TestCase):

    app_label = 'bcpp_subject'
    community = None

    def setUp(self):
        self.survey = SurveyFactory()
        site_lab_tracker.autodiscover()
        study_specific = StudySpecificFactory()
        StudySiteFactory()
        ConfigurationFactory()
        content_type_map_helper = ContentTypeMapHelper()
        content_type_map_helper.populate()
        content_type_map_helper.sync()
        content_type_map = ContentTypeMap.objects.get(content_type__model='SubjectConsent'.lower())
        ConsentCatalogueFactory(
            name=self.app_label,
            consent_type='study',
            content_type_map=content_type_map,
            version=1,
            start_datetime=study_specific.study_start_datetime,
            end_datetime=datetime(datetime.today().year + 5, 1, 1),
            add_for_app=self.app_label)
        membership_form = MembershipFormFactory(content_type_map=content_type_map)
        schedule_group = ScheduleGroupFactory(membership_form=membership_form, group_name='survey', grouping_key='SURVEY')
        visit_tracking_content_type_map = ContentTypeMap.objects.get(content_type__model='subjectvisit')
        visit_definition = VisitDefinitionFactory(code='T0', title='T0', grouping='subject', visit_tracking_content_type_map=visit_tracking_content_type_map)
        visit_definition.schedule_group.add(schedule_group)

        # add entries
        content_type_map = ContentTypeMap.objects.get(app_label='testing', model='testscheduledmodel1')
        EntryFactory(content_type_map=content_type_map, visit_definition=self.visit_definition, entry_order=100, entry_category='clinic')

        plot = PlotFactory(community=self.community, household_count=1, status='occupied')
        self.assertEqual(Plot.objects.all().count(), 1)
        self.assertEqual(Household.objects.all().count(), 1)
        self.assertEqual(HouseholdStructure.objects.all().count(), 1)
        household_structure = HouseholdStructure.objects.get(household__plot=plot)
        HouseholdMemberFactory(household_structure=household_structure)
        HouseholdMemberFactory(household_structure=household_structure)
        HouseholdMemberFactory(household_structure=household_structure)
        self.household_member_female = HouseholdMemberFactory(household_structure=household_structure, gender='F')
        self.household_member_male = HouseholdMemberFactory(household_structure=household_structure, gender='M')
        self.household_member_female.eligible_member = True
        self.household_member_male.eligible_member = True
        self.household_member_female.eligible_subject = True
        self.household_member_male.eligible_subject = True
        self.household_member_female.save()
        self.household_member_male.save()
        subject_consent_female = SubjectConsentFactory(household_member=self.household_member_female, gender='F')
        subject_consent_male = SubjectConsentFactory(household_member=self.household_member_male, gender='M')
        #FIXME: need this to be fixed, not getting gender right!
        self.registered_subject_female = RegisteredSubject.objects.get(subject_identifier=subject_consent_female.subject_identifier)
        self.registered_subject_male = RegisteredSubject.objects.get(subject_identifier=subject_consent_male.subject_identifier)
        appointment_female = Appointment.objects.get(registered_subject=self.registered_subject_female)
        self.subject_visit_female = SubjectVisitFactory(appointment=appointment_female, household_member=self.household_member_female)
        appointment_male = Appointment.objects.get(registered_subject=self.registered_subject_male)
        self.subject_visit_male = SubjectVisitFactory(appointment=appointment_male, household_member=self.household_member_male)
