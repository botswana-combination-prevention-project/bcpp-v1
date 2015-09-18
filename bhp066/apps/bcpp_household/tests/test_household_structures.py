from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

from django.test import TestCase
from django.core.exceptions import ValidationError

from edc.map.classes import site_mappers

from bhp066.apps.bcpp_household_member.models import HouseholdMember
from bhp066.apps.bcpp_household_member.tests.factories import HouseholdMemberFactory, EnrollmentChecklistFactory
from bhp066.apps.bcpp_survey.tests.factories import SurveyFactory
from bhp066.apps.bcpp_subject.tests.factories import SubjectConsentFactory

from ..models import (HouseholdIdentifierHistory, Household, HouseholdStructure, Plot, HouseholdLog,
                      PlotIdentifierHistory)

from .factories import PlotFactory, HouseholdLogEntryFactory, RepresentativeEligibilityFactory


class TestHouseholdStructures(TestCase):
    """Test plots and Households."""
    def setUp(self):
        site_mappers.autodiscover()
        self.mapper = site_mappers.get(site_mappers.get_as_list()[0])

    def test_enumerated_members1(self):
        """Assert enumerated_members defaults to False."""
        SurveyFactory()
        plot = PlotFactory(community=self.mapper().get_map_area(), household_count=3,
                           status='residential_habitable')
        for household in Household.objects.filter(plot=plot):
            for household_structure in HouseholdStructure.objects.filter(household=household):
                self.assertFalse(household_structure.enumerated)

    def test_enumerated_members2(self):
        """Assert enumerated_members is True if a household_member is added, others stay False."""
        SurveyFactory()
        plot = PlotFactory(community=self.mapper().get_map_area(), household_count=3,
                           status='residential_habitable')
        for household in Household.objects.filter(plot=plot):
            household_log = HouseholdLog.objects.get(household_structure__household=household)
        household_structure = household_log.household_structure
        RepresentativeEligibilityFactory(household_structure=household_structure)
        HouseholdMemberFactory(household_structure=household_structure)
        household_structure = HouseholdStructure.objects.get(pk=household_structure.pk)
        self.assertTrue(household_structure.enumerated)
        for household_structure in HouseholdStructure.objects.filter(household=household).exclude(pk=household_structure.pk):
            self.assertFalse(household_structure.enumerated)

    def test_eligible_members1(self):
        """Assert eligible_members set to True if an eligible member is added."""
        SurveyFactory()
        plot = PlotFactory(community=self.mapper().get_map_area(), household_count=3,
                           status='residential_habitable')
        for household in Household.objects.filter(plot=plot):
            household_log = HouseholdLog.objects.get(household_structure__household=household)
            household_log_entry = HouseholdLogEntryFactory(household_log=household_log)
        household_structure = household_log.household_structure
        RepresentativeEligibilityFactory(household_structure=household_structure)
        HouseholdMemberFactory(household_structure=household_structure)
        household_structure = HouseholdStructure.objects.get(pk=household_structure.pk)
        self.assertTrue(household_structure.eligible_members)

    def test_eligible_members2(self):
        """Assert eligible_members set from True to False if an eligible member is added then removed."""
        SurveyFactory()
        plot = PlotFactory(community=self.mapper().get_map_area(), household_count=3,
                           status='residential_habitable')
        for household in Household.objects.filter(plot=plot):
            household_log = HouseholdLog.objects.get(household_structure__household=household)
            household_log_entry = HouseholdLogEntryFactory(household_log=household_log)
        household_structure = household_log.household_structure
        RepresentativeEligibilityFactory(household_structure=household_structure)
        household_member = HouseholdMemberFactory(household_structure=household_structure)
        household_structure = HouseholdStructure.objects.get(pk=household_structure.pk)
        household_member.age_in_years = 10
        household_member.save()
        household_structure = HouseholdStructure.objects.get(pk=household_structure.pk)
        self.assertFalse(household_structure.eligible_members)

    def test_eligible_members3(self):
        """Assert eligible_members set from True but stays True if an eligible member 
        is added then removed but others exist."""
        SurveyFactory()
        plot = PlotFactory(community=self.mapper().get_map_area(), household_count=3,
                           status='residential_habitable')
        for household in Household.objects.filter(plot=plot):
            household_log = HouseholdLog.objects.get(household_structure__household=household)
            household_log_entry = HouseholdLogEntryFactory(household_log=household_log)
        household_structure = household_log.household_structure
        RepresentativeEligibilityFactory(household_structure=household_structure)
        HouseholdMemberFactory(household_structure=household_structure, age_in_years=10)
        HouseholdMemberFactory(household_structure=household_structure, age_in_years=74)
        HouseholdMemberFactory(household_structure=household_structure, age_in_years=50)
        household_member = HouseholdMemberFactory(household_structure=household_structure, age_in_years=25)
        household_structure = HouseholdStructure.objects.get(pk=household_structure.pk)
        household_member.age_in_years = 10
        household_member.save()
        self.assertTrue(household_structure.eligible_members)

    def test_enrolled1(self):
        """Assert enrolled is False if members but none consented."""
        SurveyFactory()
        plot = PlotFactory(community=self.mapper().get_map_area(), household_count=3,
                           status='residential_habitable')
        for household in Household.objects.filter(plot=plot):
            household_log = HouseholdLog.objects.get(household_structure__household=household)
            household_log_entry = HouseholdLogEntryFactory(household_log=household_log)
        household_structure = household_log.household_structure
        RepresentativeEligibilityFactory(household_structure=household_structure)
        HouseholdMemberFactory(household_structure=household_structure, age_in_years=10)
        HouseholdMemberFactory(household_structure=household_structure, age_in_years=74)
        HouseholdMemberFactory(household_structure=household_structure, age_in_years=25)
        HouseholdMemberFactory(household_structure=household_structure, age_in_years=50)
        household_structure = HouseholdStructure.objects.get(pk=household_structure.pk)
        self.assertFalse(household_structure.enrolled)

    def test_enrolled2(self):
        """Assert enrolled is True if eligible member consents."""
        SurveyFactory()
        plot = PlotFactory(community=self.mapper().get_map_area(), household_count=3,
                           status='residential_habitable')
        for household in Household.objects.filter(plot=plot):
            household_log = HouseholdLog.objects.get(household_structure__household=household)
            household_log_entry = HouseholdLogEntryFactory(household_log=household_log)
        household_structure = household_log.household_structure
        RepresentativeEligibilityFactory(household_structure=household_structure)
        HouseholdMemberFactory(household_structure=household_structure, age_in_years=10)
        HouseholdMemberFactory(household_structure=household_structure, age_in_years=74)
        household_member = HouseholdMemberFactory(
            household_structure=household_structure,
            age_in_years=25,
            initials='NN')
        HouseholdMemberFactory(household_structure=household_structure, age_in_years=50)
        household_structure = HouseholdStructure.objects.get(pk=household_structure.pk)
        dob = date.today() - relativedelta(years=25)
        enrollment_checklist = EnrollmentChecklistFactory(
            household_member=household_member,
            report_datetime=household_member.created,
            dob=dob,
            initials='NN')
        self.assertFalse(household_structure.enrolled)
        self.assertTrue(enrollment_checklist.is_eligible)
        household_member = HouseholdMember.objects.get(pk=household_member.pk)
        SubjectConsentFactory(
            household_member=household_member,
            dob=dob,
            initials='NN')
        household_structure = HouseholdStructure.objects.get(pk=household_structure.pk)
        self.assertTrue(household_structure.enrolled)
