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

from ..forms import HouseholdMemberForm


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


class HouseholdMemberTests(SimpleTestCase):

    def setUp(self):
        if Survey.objects.all().count() == 0:
            survey = SurveyFactory()
            plot = PlotFactory(community='test_community1', household_count=1, status='occupied')
            household = HouseholdFactory(plot=plot)
            self.household_structure = HouseholdStructureFactory(survey=survey, household=household)
            self.household_member = HouseholdMemberFactory(household_structure=self.household_structure)

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

