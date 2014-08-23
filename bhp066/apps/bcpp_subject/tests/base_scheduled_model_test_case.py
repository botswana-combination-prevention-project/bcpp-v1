from datetime import date
from dateutil.relativedelta import relativedelta

from django.db.models import get_model
from django.test import TestCase, TransactionTestCase, SimpleTestCase


from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.appointment.models import Appointment
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.registration.models import RegisteredSubject
from edc.core.bhp_variables.models import StudySite

from apps.bcpp.app_configuration.classes import BcppAppConfiguration
from apps.bcpp_household.models import Household, HouseholdStructure
from apps.bcpp_household.tests.factories import PlotFactory
from apps.bcpp_household_member.tests.factories import HouseholdMemberFactory, EnrollmentChecklistFactory
from apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from apps.bcpp_subject.tests.factories import SubjectConsentFactory, SubjectVisitFactory
from apps.bcpp_survey.models import Survey
from apps.bcpp_household.tests.factories import RepresentativeEligibilityFactory
from apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule


class BaseScheduledModelTestCase(TransactionTestCase):

    app_label = 'bcpp_subject'
    community = None

    def startup(self):
        HouseholdMember = get_model('bcpp_household_member', 'HouseholdMember')
        try:
            site_lab_profiles.register(BcppSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass

        BcppAppConfiguration()
        site_lab_tracker.autodiscover()
        BcppSubjectVisitSchedule().build()

        self.survey1 = Survey.objects.get(survey_name='BCPP Year 1')  # see app_configuration
        plot = PlotFactory(community=self.community, household_count=1, status='residential_habitable')
        household = Household.objects.get(plot=plot)
        household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)
        RepresentativeEligibilityFactory(household_structure=household_structure)
        HouseholdMemberFactory(household_structure=household_structure)
        HouseholdMemberFactory(household_structure=household_structure)
        HouseholdMemberFactory(household_structure=household_structure)
        self.household_member_female = HouseholdMemberFactory(household_structure=household_structure,
                                                              first_name='SUE', initials='SW', gender='F',
                                                              age_in_years=25, study_resident='Yes', relation='sister',
                                                              inability_to_participate='N/A')
        self.household_member_male = HouseholdMemberFactory(household_structure=household_structure,
                                                            first_name='ERIK', initials='EW', gender='M',
                                                            age_in_years=25, study_resident='Yes', relation='brother',
                                                            inability_to_participate='N/A')
        self.household_member_female.save()
        self.household_member_male.save()

        enrollment_male = EnrollmentChecklistFactory(
            household_member=self.household_member_male,
            initials=self.household_member_male.initials,
            gender=self.household_member_male.gender,
            dob=date.today() - relativedelta(years=self.household_member_male.age_in_years),
            guardian='N/A',
            part_time_resident='Yes',
            citizen='Yes')
        self.household_member_female = HouseholdMember.objects.get(pk=self.household_member_female.pk)
        #print self.household_member_female.member_status

        enrollment_female = EnrollmentChecklistFactory(
            household_member=self.household_member_female,
            initials=self.household_member_female.initials,
            gender=self.household_member_female.gender,
            dob=date.today() - relativedelta(years=self.household_member_female.age_in_years),
            guardian='N/A',
            part_time_resident='Yes',
            citizen='Yes')
        self.household_member_male = HouseholdMember.objects.get(pk=self.household_member_male.pk)
        #print self.household_member_male.member_status

        self.site_code = StudySite.objects.get(site_code='14')

        subject_consent_female = SubjectConsentFactory(
            household_member=self.household_member_female,
            gender='F',
            dob=enrollment_female.dob,
            first_name='SUE',
            last_name='W',
            citizen='Yes',
            initials=enrollment_female.initials,
            study_site=self.site_code)
        subject_consent_male = SubjectConsentFactory(
            household_member=self.household_member_male,
            gender='M',
            dob=enrollment_male.dob,
            first_name='ERIK',
            last_name='W',
            citizen='Yes',
            initials=enrollment_male.initials,
            study_site=self.site_code)

        # FIXME: need this to be fixed, not getting gender right!
        self.registered_subject_female = RegisteredSubject.objects.get(subject_identifier=subject_consent_female.subject_identifier)
        self.registered_subject_male = RegisteredSubject.objects.get(subject_identifier=subject_consent_male.subject_identifier)
        appointment_female = Appointment.objects.get(registered_subject=self.registered_subject_female)
        self.subject_visit_female = SubjectVisitFactory(appointment=appointment_female, household_member=self.household_member_female)
        appointment_male = Appointment.objects.get(registered_subject=self.registered_subject_male)
        self.subject_visit_male = SubjectVisitFactory(appointment=appointment_male, household_member=self.household_member_male)
