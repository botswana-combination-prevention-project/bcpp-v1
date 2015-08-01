from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

from django.test import TestCase

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.map.classes import site_mappers, Mapper
from edc.subject.appointment.models import Appointment
from edc.subject.rule_groups.classes import site_rule_groups
from edc.core.bhp_variables.models import StudySite
from edc.subject.registration.models import RegisteredSubject

from apps.bcpp_household_member.classes  import EnumerationHelper
from apps.bcpp_household.tests.factories import PlotFactory, HouseholdFactory, HouseholdStructureFactory
from apps.bcpp_household_member.tests.factories import HouseholdMemberFactory
from apps.bcpp_subject.tests.factories import SubjectConsentFactory, CorrectConsentFactory, HicEnrollmentFactory, SubjectVisitFactory, ResidencyMobilityFactory, SubjectLocatorFactory
from apps.bcpp_household_member.tests.factories import EnrollmentChecklistFactory
from apps.bcpp_household_member.models import EnrollmentChecklist, HouseholdMember
from apps.bcpp_subject.models import SubjectConsent
from apps.bcpp.app_configuration.classes import BcppAppConfiguration
from apps.bcpp_survey.models import Survey
from apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from apps.bcpp_lab.tests.factories import SubjectRequisitionFactory
from apps.bcpp_lab.models import Panel, AliquotType
from apps.bcpp_household.models import Household, HouseholdStructure
from apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule
from apps.bcpp_household.tests.factories import RepresentativeEligibilityFactory
from apps.bcpp_household.constants import (ELIGIBLE_REPRESENTATIVE_PRESENT,
                                           ELIGIBLE_REPRESENTATIVE_ABSENT, NO_HOUSEHOLD_INFORMANT,
                                           NON_RESIDENTIAL, RESIDENTIAL_NOT_HABITABLE,
                                           RESIDENTIAL_HABITABLE)
from ..models import (HivCareAdherence, HivTestingHistory, HivTestReview, HivResult, ElisaHivResult,
                      Circumcision, Circumcised, HicEnrollment, Pima)


class TestCorrectConsent(TestCase):

    app_label = 'bcpp_subject'
    community = 'otse'

    def setUp(self):
        try:
            site_lab_profiles.register(BcppSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        BcppAppConfiguration().prepare()
        site_lab_tracker.autodiscover()
        BcppSubjectVisitSchedule().build()
        site_rule_groups.autodiscover()
        self.survey = Survey.objects.all()[0]
        plot = PlotFactory(community=self.community, household_count=1, status='residential_habitable')
        survey = Survey.objects.all().order_by('datetime_start')[0]
        next_survey = Survey.objects.all().order_by('datetime_start')[1]
        study_site = StudySite.objects.get(site_code='35')
        self.study_site = StudySite.objects.get(site_code='35')

        household_structure = HouseholdStructure.objects.get(household__plot=plot, survey=survey)
        household_structure_y2 = HouseholdStructure.objects.get(household__plot=plot, survey=next_survey)
        RepresentativeEligibilityFactory(household_structure=household_structure)
        RepresentativeEligibilityFactory(household_structure=household_structure_y2)
        HouseholdMemberFactory(household_structure=household_structure)
        HouseholdMemberFactory(household_structure=household_structure)
        HouseholdMemberFactory(household_structure=household_structure)

        male_dob = date(1989, 10, 10)
        male_age_in_years = 25
        male_first_name = 'ERIK'
        male_initials = "EW"
        female_dob = date(1989, 10, 10)
        female_age_in_years = 25
        female_first_name = 'ERIKA'
        female_initials = "EW"

        self.household_member_female_T0 = HouseholdMemberFactory(household_structure=household_structure, gender='F', age_in_years=female_age_in_years, first_name=female_first_name, initials=female_initials)
        self.household_member_male_T0 = HouseholdMemberFactory(household_structure=household_structure, gender='M', age_in_years=male_age_in_years, first_name=male_first_name, initials=male_initials)
        self.household_member_female_T0.member_status = 'BHS_SCREEN'
        self.household_member_male_T0.member_status = 'BHS_SCREEN'
        self.household_member_female_T0.save()
        self.household_member_male_T0.save()
        self.enrollment_checklist_female = EnrollmentChecklistFactory(
            household_member=self.household_member_female_T0,
            gender='F',
            citizen='Yes',
            dob=female_dob,
            guardian='No',
            initials=self.household_member_female_T0.initials,
            part_time_resident='Yes')
        self.enrollment_checklist_male = EnrollmentChecklistFactory(
            household_member=self.household_member_male_T0,
            gender='M',
            citizen='Yes',
            dob=male_dob,
            guardian='No',
            initials=self.household_member_male_T0.initials,
            part_time_resident='Yes')
        self.subject_consent_female = SubjectConsentFactory(household_member=self.household_member_female_T0, study_site=study_site, gender='F', dob=female_dob, first_name=female_first_name, initials=female_initials)
        self.subject_consent_male = SubjectConsentFactory(household_member=self.household_member_male_T0, study_site=study_site, gender='M', dob=male_dob, first_name=male_first_name, initials=male_initials)

        enumeration_helper = EnumerationHelper(household_structure.household, survey, next_survey)
        self.household_member_female = enumeration_helper.create_member_on_target(self.household_member_female_T0)
        self.household_member_male = enumeration_helper.create_member_on_target(self.household_member_male_T0)

        self.registered_subject_female = RegisteredSubject.objects.get(subject_identifier=self.subject_consent_female.subject_identifier)
        self.registered_subject_male = RegisteredSubject.objects.get(subject_identifier=self.subject_consent_male.subject_identifier)
        self.appointment_female = Appointment.objects.get(registered_subject=self.registered_subject_female, visit_definition__code='T1')
        self.appointment_female_T0 = Appointment.objects.get(registered_subject=self.registered_subject_female, visit_definition__code='T0')
        self.subject_visit_female_T0 = SubjectVisitFactory(appointment=self.appointment_female_T0, household_member=self.household_member_female_T0)
        self.subject_visit_female = SubjectVisitFactory(appointment=self.appointment_female, household_member=self.household_member_female)
        self.appointment_male = Appointment.objects.get(registered_subject=self.registered_subject_male, visit_definition__code='T1')
        self.appointment_male_T0 = Appointment.objects.get(registered_subject=self.registered_subject_male, visit_definition__code='T0')
        self.subject_visit_male_T0 = SubjectVisitFactory(appointment=self.appointment_male_T0, household_member=self.household_member_male_T0)
        self.subject_visit_male = SubjectVisitFactory(appointment=self.appointment_male, household_member=self.household_member_male)

    def test_lastname_and_initials(self):
        plot = PlotFactory(
                community='test_community',
                household_count=1,
                status=RESIDENTIAL_HABITABLE,
                eligible_members=3,
                description="A blue house with yellow screen wall",
                time_of_week='Weekdays',
                time_of_day='Morning',
                gps_degrees_s=25,
                gps_minutes_s=0.5666599 + float('0.000000{}'.format(2)),
                gps_degrees_e=25,
                gps_minutes_e=44.366660 + float('0.000000{}'.format(3)),)
        household = Household.objects.get(plot=plot)
        household_structure = HouseholdStructure.objects.get(survey=self.survey, household=household)
        RepresentativeEligibilityFactory(household_structure=household_structure)
        household_member = HouseholdMemberFactory(
                            household_structure=household_structure, 
                            first_name='BAME', 
                            initials='BB', 
                            age_in_years=25,
                            gender='M')
        enrollment_checklist = EnrollmentChecklistFactory(
                                household_member=household_member, 
                                initials='BB', 
                                dob=date(1989, 10, 10),
                                gender='M',
                                guardian='N/A')
        subject_consent = SubjectConsentFactory(
                            household_member=household_member, 
                            last_name='BONNO', 
                            first_name='BAME', 
                            initials='BB', 
                            dob=date(1989, 10, 10),
                            gender='M',
                            may_store_samples='Yes',
                            study_site=self.study_site,
                            is_literate='Yes')
        correct_consent = CorrectConsentFactory(
                            subject_consent=subject_consent,
                            old_last_name='BONNO',
                            new_last_name='DIMO',
                            )
        subject_consent = SubjectConsent.objects.get(household_member=household_member)
        household_member = subject_consent.household_member
        enrollment_checklist = EnrollmentChecklist.objects.get(household_member=household_member)
        self.assertEquals(household_member.initials, 'BD')
        self.assertEquals(enrollment_checklist.initials, 'BD')
        self.assertEquals(subject_consent.initials, 'BD')
        self.assertEquals(subject_consent.last_name, 'DIMO')

    def test_firstname_and_initials(self):
        plot = PlotFactory(
                community='test_community',
                household_count=1,
                status=RESIDENTIAL_HABITABLE,
                eligible_members=3,
                description="A blue house with yellow screen wall",
                time_of_week='Weekdays',
                time_of_day='Morning',
                gps_degrees_s=25,
                gps_minutes_s=0.5666599 + float('0.000000{}'.format(2)),
                gps_degrees_e=25,
                gps_minutes_e=44.366660 + float('0.000000{}'.format(3)),)
        household = Household.objects.get(plot=plot)
        household_structure = HouseholdStructure.objects.get(survey=self.survey, household=household)
        RepresentativeEligibilityFactory(household_structure=household_structure)
        household_member = HouseholdMemberFactory(
                            household_structure=household_structure, 
                            first_name='BAME', 
                            initials='BB', 
                            age_in_years=25,
                            gender='M')
        enrollment_checklist = EnrollmentChecklistFactory(
                                household_member=household_member, 
                                initials='BB', 
                                dob=date(1989, 10, 10),
                                gender='M',
                                guardian='N/A')
        subject_consent = SubjectConsentFactory(
                            household_member=household_member, 
                            last_name='BONNO', 
                            first_name='BAME', 
                            initials='BB', 
                            dob=date(1989, 10, 10),
                            gender='M',
                            may_store_samples='Yes',
                            is_literate='Yes')
        correct_consent = CorrectConsentFactory(
                            subject_consent=subject_consent, 
                            old_first_name='BAME', 
                            new_first_name='GAME',
                            )
        subject_consent = SubjectConsent.objects.get(household_member=household_member)
        household_member = subject_consent.household_member
        enrollment_checklist = EnrollmentChecklist.objects.get(household_member=household_member)
        self.assertEquals(household_member.initials, 'GB')
        self.assertEquals(enrollment_checklist.initials, 'GB')
        self.assertEquals(subject_consent.initials, 'GB')
        self.assertEquals(household_member.first_name, 'GAME')
        self.assertEquals(subject_consent.first_name, 'GAME')

    def test_dob(self):
        household_member = self.household_member_male_T0
        enrollment_checklist = self.enrollment_checklist_male
        subject_consent = self.subject_consent_male
        hic_enrollment_options = {}
        hic_enrollment_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hicenrollment',
            appointment=self.subject_visit_male.appointment)
        ResidencyMobilityFactory(subject_visit=self.subject_visit_male_T0, intend_residency='No')
        SubjectLocatorFactory(subject_visit=self.subject_visit_male_T0, registered_subject=self.registered_subject_male, subject_cell='+26772344091')
        aliquot_type = AliquotType.objects.all()[0]
        site = StudySite.objects.all()[0]
        microtube_panel = Panel.objects.get(name='Microtube')
        micro_tube = SubjectRequisitionFactory(subject_visit=self.subject_visit_male_T0, panel=microtube_panel, aliquot_type=aliquot_type, site=site)
        HivResult.objects.create(
             subject_visit=self.subject_visit_male_T0,
             hiv_result='NEG',
             report_datetime=datetime.today(),
             insufficient_vol='No'
            )
        hic = HicEnrollmentFactory(
            subject_visit=self.subject_visit_male_T0,
            report_datetime=datetime.today(),
            hic_permission='Yes',
            permanent_resident=True,
            intend_residency=True,
            hiv_status_today='NEG',
            dob=date(1989, 10, 10),
            household_residency=True,
            citizen_or_spouse=True,
            locator_information=True,
            consent_datetime=datetime.today()
        )
        correct_consent = CorrectConsentFactory(
            subject_consent=subject_consent,
            old_dob=date(1989, 10, 10),
            new_dob=date(1988, 1, 1),
        )
        subject_consent = SubjectConsent.objects.get(
            household_member=household_member
        )
        household_member = subject_consent.household_member
        enrollment_checklist = EnrollmentChecklist.objects.get(
            household_member=household_member
        )
        hic = HicEnrollment.objects.get(subject_visit=self.subject_visit_male_T0)
        self.assertEquals(household_member.age_in_years, 27)
        self.assertEquals(enrollment_checklist.dob, date(1988, 1, 1))
        self.assertEquals(subject_consent.dob, date(1988, 1, 1))
        self.assertEquals(hic.dob, date(1988, 1, 1))

    def test_gender(self):
        plot = PlotFactory(
                community='test_community',
                household_count=1,
                status=RESIDENTIAL_HABITABLE,
                eligible_members=3,
                description="A blue house with yellow screen wall",
                time_of_week='Weekdays',
                time_of_day='Morning',
                gps_degrees_s=25,
                gps_minutes_s=0.5666599 + float('0.000000{}'.format(2)),
                gps_degrees_e=25,
                gps_minutes_e=44.366660 + float('0.000000{}'.format(3)),)
        household = Household.objects.get(plot=plot)
        household_structure = HouseholdStructure.objects.get(survey=self.survey, household=household)
        RepresentativeEligibilityFactory(household_structure=household_structure)
        household_member = HouseholdMemberFactory(
                            household_structure=household_structure, 
                            first_name='BAME', 
                            initials='BB', 
                            age_in_years=25,
                            gender='M')
        enrollment_checklist = EnrollmentChecklistFactory(
                                household_member=household_member, 
                                initials='BB', 
                                dob=date(1989, 10, 10),
                                gender='M',
                                guardian='N/A')
        subject_consent = SubjectConsentFactory(
                            household_member=household_member, 
                            last_name='BONNO', 
                            first_name='BAME', 
                            initials='BB', 
                            dob=date(1989, 10, 10),
                            gender='M',
                            may_store_samples='Yes',
                            is_literate='Yes')
        correct_consent = CorrectConsentFactory(
                            subject_consent=subject_consent, 
                            old_gender='M', 
                            new_gender='F',
                            )
        subject_consent = SubjectConsent.objects.get(household_member=household_member)
        household_member = subject_consent.household_member
        enrollment_checklist = EnrollmentChecklist.objects.get(household_member=household_member)
        self.assertEquals(household_member.gender, 'F')
        self.assertEquals(enrollment_checklist.gender, 'F')
        self.assertEquals(subject_consent.gender, 'F')

    def test_witness(self):
        plot = PlotFactory(
                community='test_community',
                household_count=1,
                status=RESIDENTIAL_HABITABLE,
                eligible_members=3,
                description="A blue house with yellow screen wall",
                time_of_week='Weekdays',
                time_of_day='Morning',
                gps_degrees_s=25,
                gps_minutes_s=0.5666599 + float('0.000000{}'.format(2)),
                gps_degrees_e=25,
                gps_minutes_e=44.366660 + float('0.000000{}'.format(3)),)
        household = Household.objects.get(plot=plot)
        household_structure = HouseholdStructure.objects.get(survey=self.survey, household=household)
        RepresentativeEligibilityFactory(household_structure=household_structure)
        household_member = HouseholdMemberFactory(
                            household_structure=household_structure, 
                            first_name='BAME', 
                            initials='BB', 
                            age_in_years=25,
                            gender='M')
        enrollment_checklist = EnrollmentChecklistFactory(
                                household_member=household_member, 
                                initials='BB', 
                                dob=date(1989, 10, 10),
                                gender='M',
                                guardian='N/A')
        subject_consent = SubjectConsentFactory(
                            household_member=household_member,
                            last_name='BONNO',
                            first_name='BAME',
                            initials='BB',
                            dob=date(1989, 10, 10),
                            gender='M',
                            may_store_samples='Yes',
                            is_literate='No',
                            witness_name='DIMO')
        correct_consent = CorrectConsentFactory(
                            subject_consent=subject_consent,
                            old_witness_name='DIMO',
                            new_witness_name='BIMO',
                            )
        subject_consent = SubjectConsent.objects.get(household_member=household_member)
        household_member = subject_consent.household_member
        enrollment_checklist = EnrollmentChecklist.objects.get(household_member=household_member)
        self.assertEquals(subject_consent.witness_name, 'BIMO')
