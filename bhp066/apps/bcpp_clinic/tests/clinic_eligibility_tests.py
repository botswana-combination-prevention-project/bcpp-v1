from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from uuid import uuid4

from django.test import TestCase
from django.core.exceptions import ValidationError

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc_constants.constants import NOT_APPLICABLE
from edc.core.bhp_variables.models import StudySite
from edc.subject.visit_schedule.classes import site_visit_schedules

from bhp066.apps.bcpp.app_configuration.classes import bcpp_app_configuration
from bhp066.apps.bcpp_household.models import Household, HouseholdStructure
from bhp066.apps.bcpp_household_member.models import HouseholdMember
from bhp066.apps.bcpp_household.tests.factories import PlotFactory
from bhp066.apps.bcpp_household_member.tests.factories import HouseholdMemberFactory, EnrollmentChecklistFactory
from bhp066.apps.bcpp_household.utils.survey_dates_tuple import SurveyDatesTuple

from bhp066.apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from bhp066.apps.bcpp_subject.tests.factories import SubjectConsentFactory
from bhp066.apps.bcpp_survey.models import Survey
from bhp066.apps.bcpp_household.tests.factories import RepresentativeEligibilityFactory
from edc.map.classes import site_mappers

from ..models import ClinicEligibility
from .factories import ClinicConsentFactory


class ClinicEligibilityTests(TestCase):
    def __init__(self, *args, **kwargs):
        self.household_member = None
        self.subject_consent = None
        self.enrollment_checklist = None
        self.registered_subject = None
        self.study_site = None
        super(ClinicEligibilityTests, self).__init__(*args, **kwargs)

    def setUp(self):
        site_mappers.autodiscover()

        try:
            site_lab_profiles.register(BcppSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        mapper = site_mappers._registry_by_code.get('01')
        mapper.survey_dates = {
            'bcpp-year-1': SurveyDatesTuple(
                name='bhs',
                start_date=date.today() + relativedelta(years=-1) + relativedelta(days=-89),
                full_enrollment_date=date.today() + relativedelta(years=-1) + relativedelta(days=60),
                end_date=date.today() + relativedelta(years=-1) + relativedelta(days=89),
                smc_start_date=date.today() + relativedelta(years=-1) + relativedelta(days=89)),
            'bcpp-year-2': SurveyDatesTuple(
                name='t1',
                start_date=date.today() + relativedelta(years=0) + relativedelta(days=-89),
                full_enrollment_date=date.today() + relativedelta(years=0) + relativedelta(days=60),
                end_date=date.today() + relativedelta(years=0) + relativedelta(days=89),
                smc_start_date=date.today() + relativedelta(years=0) + relativedelta(days=89)),
        }

        bcpp_app_configuration.survey_setup = {
            'bcpp-year-1':
                {'survey_name': 'BCPP Year 1',
                 'survey_slug': 'bcpp-year-1',
                 'datetime_start': datetime.today() + relativedelta(years=-1) + relativedelta(days=-30),
                 'datetime_end': datetime.today() + relativedelta(years=-1) + relativedelta(days=30)},
            'bcpp-year-2':
                {'survey_name': 'BCPP Year 2',
                 'survey_slug': 'bcpp-year-2',
                 'datetime_start': datetime.today() + relativedelta(days=-90),
                 'datetime_end': datetime.today() + relativedelta(days=90)},
            'bcpp-year-3':
                {'survey_name': 'BCPP Year 3',
                 'survey_slug': 'bcpp-year-3',
                 'datetime_start': datetime.today() + relativedelta(years=1) + relativedelta(days=-30),
                 'datetime_end': datetime.today() + relativedelta(years=1) + relativedelta(days=30)},
        }

        bcpp_app_configuration.prepare()
        site_lab_tracker.autodiscover()
        site_visit_schedules.autodiscover()
        site_visit_schedules.build_all()

        self.survey2 = Survey.objects.current_survey()
        self.survey1 = Survey.objects.previous_survey()
        plot = PlotFactory(community='test_community', household_count=1, status='residential_habitable')
        self.household = Household.objects.get(plot=plot)
        self.source_household_structure = HouseholdStructure.objects.get(household=self.household, survey=self.survey1)
        self.target_household_structure = HouseholdStructure.objects.get(household=self.household, survey=self.survey2)
        self.representative_eligibility = RepresentativeEligibilityFactory(household_structure=self.source_household_structure)
        self.study_site = StudySite.objects.get(site_code=site_mappers.get_current_mapper().map_code)
        self.intervention = site_mappers.get_current_mapper().intervention
        site_mappers.get_current_mapper().verify_survey_dates()

        # add members to source
        HouseholdMemberFactory(household_structure=self.source_household_structure)
        HouseholdMemberFactory(household_structure=self.source_household_structure)
        HouseholdMemberFactory(household_structure=self.source_household_structure)
        HouseholdMemberFactory(household_structure=self.source_household_structure)
        self.household_member_female = HouseholdMemberFactory(household_structure=self.source_household_structure,
                                                              first_name='SUE', initials='SW', gender='F',
                                                              age_in_years=25, study_resident='Yes', relation='sister',
                                                              inability_to_participate=NOT_APPLICABLE)

        enrollment_female = EnrollmentChecklistFactory(
            household_member=self.household_member_female,
            initials=self.household_member_female.initials,
            gender=self.household_member_female.gender,
            dob=date.today() - relativedelta(years=self.household_member_female.age_in_years),
            guardian=NOT_APPLICABLE,
            part_time_resident='Yes',
            citizen='Yes')
        SubjectConsentFactory(
            household_member=self.household_member_female,
            gender='F',
            dob=enrollment_female.dob,
            first_name='SUE',
            last_name='W',
            citizen='Yes',
            identity='111121111',
            initials=enrollment_female.initials,
            study_site=self.study_site)

    def test_additional_key1(self):
        """Tests constraint across hhm, clinic_eligibility and registered_subject
        unique_together = ['first_name', 'initials', 'identity', 'additional_key']"""
        clinic_eligibility = ClinicEligibility(
            report_datetime=datetime.today(),
            first_name='ERIK',
            initials='EW',
            age_in_years=50,
            identity=None,
            identity_type='OMANG',
        )
        clinic_eligibility.save()
        self.assertIsInstance(clinic_eligibility.additional_key, uuid4().__class__)
        self.assertEquals(clinic_eligibility.additional_key, clinic_eligibility.household_member.additional_key)
        self.assertEquals(clinic_eligibility.additional_key, clinic_eligibility.household_member.registered_subject.additional_key)

    def test_additional_key2(self):
        """Assert that eligibility will not save if subject already consented."""
        clinic_eligibility = ClinicEligibility(
            report_datetime=datetime.today(),
            first_name='SUE',
            initials='SW',
            dob=date(1964, 5, 27),
            identity='111121112',
            identity_type='OMANG',
            gender='F',
        )
        clinic_eligibility.save()

        clinic_eligibility = ClinicEligibility.objects.get(pk=clinic_eligibility.pk)

        ClinicConsentFactory(
            household_member=clinic_eligibility.household_member,
            gender='F',
            dob=clinic_eligibility.dob,
            first_name='SUE',
            last_name='W',
            citizen='Yes',
            identity='111121112',
            identity_type='OMANG',
            initials=clinic_eligibility.initials,
            study_site=self.study_site)

        clinic_eligibility = ClinicEligibility(
            report_datetime=datetime.today(),
            first_name='BARBARA',
            initials='BW',
            dob=date(1964, 5, 27),
            identity='111121112',
            identity_type='OMANG',
            gender='F',
        )
        self.assertRaises(ValidationError, clinic_eligibility.save)

    def test_additional_key3(self):
        """Assert that eligibility will not save if subject already consented."""
        clinic_eligibility = ClinicEligibility(
            report_datetime=datetime.today(),
            first_name='SUE',
            initials='SW',
            dob=date(1964, 5, 27),
            identity='111121111',
            identity_type='OMANG',
            gender='F',
        )
        self.assertRaises(ValidationError, clinic_eligibility.save)

    def test_additional_key4(self):
        """Tests constraint across hhm, clinic_eligibility and registered_subject
        unique_together = ['first_name', 'initials', 'identity', 'additional_key']"""
        self.assertEquals(HouseholdMember.objects.all().count(), 5)
        clinic_eligibility = ClinicEligibility(
            report_datetime=datetime.today(),
            first_name='ERIK',
            initials='EW',
            dob=date(1964, 5, 27),
            identity='111111134',
            identity_type='OMANG',
        )
        clinic_eligibility.save()
        self.assertEquals(clinic_eligibility.additional_key, None)
        self.assertEquals(clinic_eligibility.additional_key, clinic_eligibility.household_member.additional_key)
        self.assertEquals(clinic_eligibility.additional_key, clinic_eligibility.household_member.registered_subject.additional_key)
        self.assertEquals(HouseholdMember.objects.all().count(), 6)

        clinic_eligibility = ClinicEligibility(
            report_datetime=datetime.today(),
            first_name='ERIK',
            initials='EW',
            dob=date(1964, 5, 27),
            identity=None,
            identity_type='OMANG',
        )
        clinic_eligibility.save()
        self.assertIsInstance(clinic_eligibility.additional_key, uuid4().__class__)
        self.assertEquals(clinic_eligibility.additional_key, clinic_eligibility.household_member.additional_key)
        self.assertEquals(clinic_eligibility.additional_key, clinic_eligibility.household_member.registered_subject.additional_key)

        # add with same OMANG, shoulf fail
        clinic_eligibility = ClinicEligibility(
            report_datetime=datetime.today(),
            first_name='ERIK',
            initials='EW',
            dob=date(1964, 5, 27),
            identity='111111134',
            identity_type='OMANG',
        )
        self.assertRaises(ValidationError, clinic_eligibility.save)

        # add with different OMANG, all other values the same, should succeed
        clinic_eligibility = ClinicEligibility(
            report_datetime=datetime.today(),
            first_name='ERIK',
            initials='EW',
            dob=date(1964, 5, 27),
            identity='111111112',
            identity_type='OMANG',
        )
        self.assertIsNone(clinic_eligibility.save())
        # specified identity so additional_key must be None
        self.assertEquals(clinic_eligibility.additional_key, None)
        self.assertEquals(clinic_eligibility.additional_key, clinic_eligibility.household_member.additional_key)
        self.assertEquals(clinic_eligibility.additional_key, clinic_eligibility.household_member.registered_subject.additional_key)

        self.assertEquals(HouseholdMember.objects.all().count(), 8)
