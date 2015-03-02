from django.test import TestCase
from django.db.models import signals
from django.forms import ValidationError

from edc.map.classes import Mapper, site_mappers
from apps.bcpp_household.tests.factories import PlotFactory, HouseholdFactory, HouseholdStructureFactory
from apps.bcpp_survey.models import Survey
from apps.bcpp_survey.tests.factories import SurveyFactory
from apps.bcpp_household.models import household_structure_on_post_save
#from apps.bcpp_subject.models import SubjectConsent
from .factories import SubjectAbsenteeEntryFactory

from ..models import SubjectAbsentee

from ..forms import HouseholdMemberForm

from .factories import HouseholdMemberFactory


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
        if Survey.objects.all().count() == 0:
            survey = SurveyFactory()
            plot = PlotFactory(community='test_community1', household_count=1, status='occupied')
            household = HouseholdFactory(plot=plot)
            self.household_structure = HouseholdStructureFactory(survey=survey, household=household)
            self.household_member = HouseholdMemberFactory(household_structure=self.household_structure)
        signals.post_save.connect(household_structure_on_post_save, weak=False, dispatch_uid="household_structure_on_post_save")

    def test_relation_to_head(self):
        """Cannot allow more than one member to be Head of Household."""
        self.household_member.relation = 'Head'
        self.household_member.save()
        form = HouseholdMemberForm()
        form.cleaned_data = {'first_name': u'THABO',
                               'gender': u'M',
                               'household_structure': self.household_member.household_structure,
                               'study_resident': u'Yes',
                               'present_today': u'No',
                               'relation': u'Head',
                               'age_in_years': 32,
                               'initials': u'TM'}
        self.assertRaisesRegexp(ValidationError, 'Head of Household ', form.clean)

    def test_updating_on_absentee_entry(self):
        from ..models import HouseholdMember
        self.household_member.member_status = 'ABSENT'
        self.household_member.save()
        self.assertEquals(self.household_member.absentee_visit_attempts, 0)
        absentee_entry1 = SubjectAbsenteeEntryFactory(subject_absentee=self.household_member.subject_absentee)
        self.assertEquals(HouseholdMember.objects.get(id=self.household_member.id).absentee_visit_attempts, 1)
        absentee_entry2 = SubjectAbsenteeEntryFactory(subject_absentee=self.household_member.subject_absentee)
        self.assertEquals(HouseholdMember.objects.get(id=self.household_member.id).absentee_visit_attempts, 2)
        absentee_entry3 = SubjectAbsenteeEntryFactory(subject_absentee=self.household_member.subject_absentee)
        self.assertEquals(HouseholdMember.objects.get(id=self.household_member.id).absentee_visit_attempts, 3)
        self.assertTrue(HouseholdMember.objects.get(id=self.household_member.id).absentee)

    def creates_absentee(self):
        """Test creates an absentee instance if participation changed to absent."""
        self.assertEquals(SubjectAbsentee.objects.filter(household_member=self.household_member).count(), 0)
        self.household_member.member_status = 'ABSENT'
        self.household_member.save()
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
