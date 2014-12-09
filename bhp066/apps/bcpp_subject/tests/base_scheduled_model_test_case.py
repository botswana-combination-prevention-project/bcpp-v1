from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from django.db.models import get_model
from django.test import TestCase, TransactionTestCase, SimpleTestCase

from edc.map.classes import site_mappers
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.appointment.models import Appointment
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.registration.models import RegisteredSubject
from edc.core.bhp_variables.models import StudySite
from edc.constants import NOT_APPLICABLE
from edc.subject.visit_schedule.classes import site_visit_schedules
from apps.bcpp.app_configuration.classes import bcpp_app_configuration

# from apps.bcpp.app_configuration.classes import BcppAppConfiguration
from apps.bcpp_household.models import Household, HouseholdStructure
from apps.bcpp_household.tests.factories import PlotFactory
from apps.bcpp_household_member.tests.factories import HouseholdMemberFactory, EnrollmentChecklistFactory
from apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from apps.bcpp_subject.tests.factories import SubjectConsentFactory, SubjectVisitFactory
from apps.bcpp_survey.models import Survey
from apps.bcpp_household.tests.factories import RepresentativeEligibilityFactory
from apps.bcpp_household.utils.survey_dates_tuple import SurveyDatesTuple


class BaseScheduledModelTestCase(TestCase):

    app_label = 'bcpp_subject'
    community = None
    site_code = None
    study_site = None

    def startup(self):
        
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

        self.household_structure = None
        self.registered_subject = None
        self.representative_eligibility = None
        self.study_site = None
        self.intervention = None
#         try:
#             site_lab_profiles.register(BcppSubjectProfile())
#         except AlreadyRegisteredLabProfile:
#             pass
#         BcppAppConfiguration()
#         site_lab_tracker.autodiscover()
#         BcppSubjectVisitSchedule().build()

        self.community = site_mappers.get_current_mapper().map_area
        self.study_site = StudySite.objects.get(site_code=site_mappers.get_current_mapper().map_code)
        self.site_code = self.study_site
        self.intervention = site_mappers.get_current_mapper().intervention
        self.survey1 = Survey.objects.get(survey_name='BCPP Year 1')  # see app_configuration
        plot = PlotFactory(community=self.community, household_count=1, status='residential_habitable')
        household = Household.objects.get(plot=plot)
        household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)
        RepresentativeEligibilityFactory(household_structure=household_structure)
        HouseholdMemberFactory(household_structure=household_structure)
        HouseholdMemberFactory(household_structure=household_structure)
        HouseholdMemberFactory(household_structure=household_structure)

        HouseholdMember = get_model('bcpp_household_member', 'HouseholdMember')

        self.household_member_female = HouseholdMemberFactory(household_structure=household_structure,
                                                              first_name='SUE', initials='SW', gender='F',
                                                              age_in_years=25, study_resident='Yes', relation='sister',
                                                              inability_to_participate=NOT_APPLICABLE)
        self.household_member_male = HouseholdMemberFactory(household_structure=household_structure,
                                                            first_name='ERIK', initials='EW', gender='M',
                                                            age_in_years=25, study_resident='Yes', relation='brother',
                                                            inability_to_participate=NOT_APPLICABLE)
        self.household_member_female.save()
        self.household_member_male.save()

        enrollment_male = EnrollmentChecklistFactory(
            household_member=self.household_member_male,
            initials=self.household_member_male.initials,
            gender=self.household_member_male.gender,
            dob=date.today() - relativedelta(years=self.household_member_male.age_in_years),
            guardian=NOT_APPLICABLE,
            part_time_resident='Yes',
            citizen='Yes')
        self.household_member_female = HouseholdMember.objects.get(pk=self.household_member_female.pk)
        # print self.household_member_female.member_status

        enrollment_female = EnrollmentChecklistFactory(
            household_member=self.household_member_female,
            initials=self.household_member_female.initials,
            gender=self.household_member_female.gender,
            dob=date.today() - relativedelta(years=self.household_member_female.age_in_years),
            guardian=NOT_APPLICABLE,
            part_time_resident='Yes',
            citizen='Yes')
        self.household_member_male = HouseholdMember.objects.get(pk=self.household_member_male.pk)
        # print self.household_member_male.member_status

        subject_consent_female = SubjectConsentFactory(
            household_member=self.household_member_female,
            gender='F',
            dob=enrollment_female.dob,
            first_name='SUE',
            last_name='W',
            citizen='Yes',
            initials=enrollment_female.initials,
            study_site=self.study_site)
        subject_consent_male = SubjectConsentFactory(
            household_member=self.household_member_male,
            gender='M',
            dob=enrollment_male.dob,
            first_name='ERIK',
            last_name='W',
            citizen='Yes',
            initials=enrollment_male.initials,
            study_site=self.study_site)

        # FIXME: need this to be fixed, not getting gender right!
        self.registered_subject_female = RegisteredSubject.objects.get(subject_identifier=subject_consent_female.subject_identifier)
        self.registered_subject_male = RegisteredSubject.objects.get(subject_identifier=subject_consent_male.subject_identifier)
        appointment_female = Appointment.objects.get(registered_subject=self.registered_subject_female, visit_definition__time_point=0)
        self.subject_visit_female = SubjectVisitFactory(appointment=appointment_female, household_member=self.household_member_female)
        appointment_male = Appointment.objects.get(registered_subject=self.registered_subject_male, visit_definition__time_point=0)
        self.subject_visit_male = SubjectVisitFactory(appointment=appointment_male, household_member=self.household_member_male)
