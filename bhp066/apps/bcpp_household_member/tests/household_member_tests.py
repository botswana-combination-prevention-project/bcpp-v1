from django.test import TestCase
from django.db.models import signals
from django.forms import ValidationError
from django.core.exceptions import ImproperlyConfigured

from edc_map.classes import Mapper, site_mappers
from bhp066.apps.bcpp_household.tests.factories import PlotFactory, HouseholdFactory, HouseholdStructureFactory, RepresentativeEligibilityFactory
from bhp066.apps.bcpp_survey.models import Survey
from bhp066.apps.bcpp_survey.tests.factories import SurveyFactory
from bhp066.apps.bcpp_household.models import household_structure_on_post_save
#from bhp066.apps.bcpp_subject.models import SubjectConsent
from .factories import SubjectAbsenteeEntryFactory

from ..models import SubjectAbsentee

from ..forms import HouseholdMemberForm

from .factories import HouseholdMemberFactory


from datetime import datetime
from django.conf import settings
from django import forms
from django.core.exceptions import ValidationError
from django.test import TestCase
 
from edc_map.classes import site_mappers, Mapper
from edc.map.exceptions import MapperError


from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups

from bhp066.apps.bcpp.app_configuration.classes import BcppAppConfiguration
from bhp066.apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from bhp066.apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule
from bhp066.apps.bcpp_household_member.constants import HEAD_OF_HOUSEHOLD


class TestPlotMapper(Mapper):
    map_area = 'test_community1'
    map_code = '099'
    regions = []
    sections = []
    landmarks = []
    gps_center_lat = -25.033194
    gps_center_lon = 25.747132
    radius = 5.5
    location_boundary = ()

site_mappers.register(TestPlotMapper)


class HouseholdMemberTests(TestCase):

    def setUp(self):

        signals.post_save.disconnect(household_structure_on_post_save, weak=False, dispatch_uid="household_structure_on_post_save")
        BcppAppConfiguration().prepare()
        self.plot = PlotFactory(community='test_community1', household_count=1, status='residential_not_habitable')  # occupied
        self.household = HouseholdFactory(plot=self.plot)
        self.survey = SurveyFactory()
        self.household_structure = HouseholdStructureFactory(survey=self.survey, household=self.household)
        RepresentativeEligibilityFactory(household_structure=self.household_structure)
        self.household_member = HouseholdMemberFactory(household_structure=self.household_structure)
        signals.post_save.connect(household_structure_on_post_save, weak=False, dispatch_uid="household_structure_on_post_save")

    def test_relation_to_head(self):
        """Cannot allow more than one member to be Head of Household."""
        self.household_member.relation = HEAD_OF_HOUSEHOLD
        self.household_member.save()
        form = HouseholdMemberForm()
        form.cleaned_data = {'first_name': u'THABO',
                               'gender': u'M',
                               'household_structure': self.household_member.household_structure,
                               'study_resident': u'Yes',
                               'present_today': u'No',
                               'relation': HEAD_OF_HOUSEHOLD,
                               'age_in_years': 32,
                               'initials': u'TM'}
        self.assertRaises(ValidationError, form.clean)  # 'Head of Household '

    def test_updating_on_absentee_entry(self):
        """Test creates an absentee instance if participation changed to absent."""
        from ..models import HouseholdMember
        self.household_member.member_status = 'ABSENT'
        self.household_member.save()
#
        SubjectAbsenteeEntryFactory(household_member=self.household_member)
        self.assertEquals(SubjectAbsentee.objects.filter(household_member=self.household_member).count(), 1)
        SubjectAbsenteeEntryFactory(household_member=self.household_member)
        self.assertEquals(SubjectAbsentee.objects.filter(household_member=self.household_member).count(), 2)
        SubjectAbsenteeEntryFactory(household_member=self.household_member)
        self.assertEquals(SubjectAbsentee.objects.filter(household_member=self.household_member).count(), 3)
        self.assertTrue(HouseholdMember.objects.get(id=self.household_member.id).absent)
# #         #
#         absentee_entry2 = SubjectAbsenteeEntryFactory(subject_absentee=self.household_member.subject_absentee)
#         self.assertEquals(HouseholdMember.objects.get(id=self.household_member.id).absentee_visit_attempts, 2)
#         #
#         absentee_entry3 = SubjectAbsenteeEntryFactory(subject_absentee=self.household_member.subject_absentee)
#         self.assertEquals(HouseholdMember.objects.get(id=self.household_member.id).absentee_visit_attempts, 3)
#         self.assertTrue(HouseholdMember.objects.get(id=self.household_member.id).absentee)

    def creates_absentee(self):
        """Test creates an absentee instance if participation changed to absent."""
        self.household_member.member_status = 'ABSENT'
        self.household_member.save()
        SubjectAbsenteeEntryFactory(household_member=self.household_member)
        self.assertEquals(SubjectAbsentee.objects.filter(household_member=self.household_member).count(), 1)

    def creates_absentee2(self):
        """Test does not create an absentee instance if already exists."""
        self.assertEquals(SubjectAbsentee.objects.filter(household_member=self.household_member).count(), 0)
        self.household_member.member_status = 'ABSENT'
        self.household_member.save()
        self.household_member.member_status = 'NOT_REPORTED'
        self.household_member.save()
        self.assertEquals(SubjectAbsentee.objects.filter(household_member=self.household_member).count(), 1)
        self.household_member.member_status = 'ABSENT'
        self.household_member.save()
        self.assertEquals(SubjectAbsentee.objects.filter(household_member=self.household_member).count(), 1)

    def creates_absentee3(self):
        """Test does not create an absentee instance if not absent and returns None."""
        # never been absent, return None
        self.household_member.member_status = 'NOT_REPORTED'
        self.household_member.save()
        self.assertIsNone(self.household_member.subject_absentee)
        self.assertEquals(SubjectAbsentee.objects.filter(household_member=self.household_member).count(), 0)
        # absent, return instance
        self.household_member.member_status = 'ABSENT'
        self.household_member.save()
        self.assertIsNotNone(self.household_member.subject_absentee)
        self.assertEquals(SubjectAbsentee.objects.filter(household_member=self.household_member).count(), 1)
        # was absent but is no longer, return instance
        self.household_member.member_status = 'NOT_REPORTED'
        self.household_member.save()
        self.assertIsNotNone(self.household_member.subject_absentee)
        self.assertEquals(SubjectAbsentee.objects.filter(household_member=self.household_member).count(), 1)

    def test_validate_household_member_create_invalid(self):
        """ Test whether the household_member cannot be created in the wrong survey."""
        household_structure = HouseholdStructureFactory(survey=SurveyFactory(), household=self.household)
        RepresentativeEligibilityFactory(household_structure=household_structure)
        hhm = HouseholdMemberFactory(household_structure=household_structure)
        self.assertRaises(ImproperlyConfigured, hhm.save())

    def test_validate_household_member_create_valid(self):
        """ Test whether the household_member it is created with the current survey."""
        from ..models import HouseholdMember
        HouseholdMemberFactory(household_structure=self.household_structure)
        self.assertEqual(HouseholdMember.objects.filter(household_structure=self.household_structure).count(), 2)

