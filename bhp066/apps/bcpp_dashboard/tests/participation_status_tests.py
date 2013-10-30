from datetime import datetime, timedelta
from dateutils import relativedelta
from uuid import uuid4
from django.test import TransactionTestCase, TestCase, SimpleTestCase
from django.db.models import signals
from django.forms import ValidationError
from edc.map.classes import Mapper, site_mappers
from edc.core.bhp_variables.tests.factories import StudySiteFactory
from edc.subject.appointment_helper.models import prepare_appointments_on_post_save
from apps.bcpp_survey.tests.factories import SurveyFactory
from apps.bcpp_household.tests.factories import PlotFactory, HouseholdFactory, HouseholdStructureFactory

from apps.bcpp_survey.models import Survey
from apps.bcpp_household_member.models import HouseholdMember
from apps.bcpp_household.models import HouseholdStructure, Household, Plot
from apps.bcpp_household_member.tests.factories import HouseholdMemberFactory
from apps.bcpp_subject.models import SubjectAbsentee, SubjectAbsenteeEntry, SubjectConsent

# from apps.bcpp_subject.tests.factories import SubjectAbsenteeEntryFactory
from ..views.participation import update_member_status


class TestPlotMapper(Mapper):
    map_area = 'test_community3'
    map_code = '091'
    regions = []
    sections = []
    landmarks = []
    gps_center_lat = -25.033194
    gps_center_lon = 25.747139
    radius = 5.5
    location_boundary = ()

site_mappers.register(TestPlotMapper)


class ParticipationStatusTests(TestCase):

    def setUp(self):
        if Survey.objects.all().count() == 0:
            survey = SurveyFactory()
            plot = PlotFactory(community='test_community3', household_count=1, status='occupied')
            household = Household.objects.get(plot=plot)
            household_structure = HouseholdStructure.objects.get(household=household)
            self.household_member = HouseholdMemberFactory(household_structure=household_structure)

    def test_new_is_not_reported(self):
        """new member by default is NOT_REPORTED."""
        self.assertEqual(self.household_member.member_status, 'NOT_REPORTED')

    def test_change_absent(self):
        """new member changed to absent and created a subject_absentee instance."""
        self.assertEqual(SubjectAbsentee.objects.filter(household_member=self.household_member).count(), 0)
        cleaned_data = {'status': 'ABSENT'}
        new_status = update_member_status(self.household_member, cleaned_data)
        self.assertEqual('ABSENT', new_status)
        self.assertEqual(SubjectAbsentee.objects.filter(household_member=self.household_member).count(), 1)

    def test_change_to_absent_and_back1(self):
        """new member changed from absent and deletes a subject_absentee instance if no entries."""
        self.assertEqual(SubjectAbsentee.objects.filter(household_member=self.household_member).count(), 0)
        cleaned_data = {'status': 'ABSENT'}
        new_status = update_member_status(self.household_member, cleaned_data)
        #self.assertEqual('ABSENT', new_status)
        #self.assertEqual(SubjectAbsentee.objects.filter(household_member=self.household_member).count(), 1)
        self.assertEqual(SubjectAbsentee.objects.filter(household_member=self.household_member).count(), 1)
        self.assertEqual(self.household_member.member_status, new_status)
        cleaned_data = {'status': 'NOT_REPORTED'}
        new_status = update_member_status(self.household_member, cleaned_data)
        self.assertEqual(SubjectAbsentee.objects.filter(household_member=self.household_member).count(), 0)

    def test_change_to_absent_and_back2(self):
        """new member changed from absent and does not delete the subject_absentee instance with entries."""
        self.assertEqual(SubjectAbsentee.objects.filter(household_member=self.household_member).count(), 0)
        cleaned_data = {'status': 'ABSENT'}
        new_status = update_member_status(self.household_member, cleaned_data)
        #self.assertEqual('ABSENT', new_status)
        #self.assertEqual(SubjectAbsentee.objects.filter(household_member=self.household_member).count(), 1)
        self.assertEqual(SubjectAbsentee.objects.filter(household_member=self.household_member).count(), 1)
        # not using factory becuase there is an import error. TODO: need to track it down
        SubjectAbsenteeEntry.objects.create(
            subject_absentee=SubjectAbsentee.objects.get(household_member=self.household_member),
            report_datetime=datetime.today(),
            reason='reason',
            next_appt_datetime=datetime.today() + timedelta(days=10),
            next_appt_datetime_source='erik')
        self.assertEqual(self.household_member.member_status, new_status)
        cleaned_data = {'status': 'NOT_REPORTED'}
        new_status = update_member_status(self.household_member, cleaned_data)
        self.assertEqual(SubjectAbsentee.objects.filter(household_member=self.household_member).count(), 1)

    def test_change_from_research1(self):
        """change from research to something else and clear eligible_subject if true."""
        self.household_member.eligible_subject = True
        self.household_member.member_status = 'RESEARCH'
        self.household_member.save()
        self.assertTrue(self.household_member.eligible_subject)
        cleaned_data = {'status': 'REFUSED'}
        new_status = update_member_status(self.household_member, cleaned_data)
        self.assertFalse(self.household_member.eligible_subject)
        self.assertEqual(self.household_member.member_status, 'REFUSED')

    def test_change_from_research2(self):
        """change from research with consent to something else, should not clear eligible_subject and not change."""
        signals.post_save.disconnect(prepare_appointments_on_post_save, weak=False, dispatch_uid='prepare_appointments_on_post_save')
        self.household_member.eligible_subject = True
        self.household_member.member_status = 'RESEARCH'
        self.household_member.save()
        self.assertTrue(self.household_member.eligible_subject)
        SubjectConsent.objects.create(  # TODO: replace with factory
            household_member=self.household_member,
            registered_subject=self.household_member.registered_subject,
            survey=self.household_member.household_structure.survey,
            identity='111111111',
            identity_type='OMANG',
            gender='M',
            first_name='ERIK',
            last_name='ERIK',
            initials='EE',
            study_site=StudySiteFactory(),
            consent_datetime=datetime.today(),
            may_store_samples='Yes',
            is_incarcerated='No',
            is_literate='Yes',
            )
        cleaned_data = {'status': 'REFUSED'}
        new_status = update_member_status(self.household_member, cleaned_data)
        self.assertTrue(self.household_member.eligible_subject)
        self.assertEqual(self.household_member.member_status, 'RESEARCH')