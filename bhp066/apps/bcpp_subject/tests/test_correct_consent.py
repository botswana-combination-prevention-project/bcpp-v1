from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from django.test import TestCase

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.appointment.models import Appointment
from edc.subject.rule_groups.classes import site_rule_groups
from edc.core.bhp_variables.models import StudySite
from edc.subject.registration.models import RegisteredSubject

from bhp066.apps.bcpp_household_member.classes import EnumerationHelper
from bhp066.apps.bcpp_household.tests.factories import PlotFactory
from bhp066.apps.bcpp_household_member.tests.factories import HouseholdMemberFactory, EnrollmentChecklistFactory
from bhp066.apps.bcpp_subject.tests.factories import SubjectConsentFactory, CorrectConsentFactory, SubjectVisitFactory
from bhp066.apps.bcpp_household_member.models import HouseholdMember, EnrollmentChecklist
from bhp066.apps.bcpp.app_configuration.classes import BcppAppConfiguration
from bhp066.apps.bcpp_survey.models import Survey
from bhp066.apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from bhp066.apps.bcpp_household.models import HouseholdStructure
from bhp066.apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule
from bhp066.apps.bcpp_household.tests.factories import RepresentativeEligibilityFactory

from ..models import SubjectConsent


class TestCorrectConsent(TestCase):

    app_label = 'bcpp_subject'
    community = 'nata'

    def setUp(self):
        try:
            site_lab_profiles.register(BcppSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        BcppAppConfiguration().prepare()
        site_lab_tracker.autodiscover()
        BcppSubjectVisitSchedule().build()
        site_rule_groups.autodiscover()
        self.study_site = StudySite.objects.get(site_code='38')
        self.survey = Survey.objects.all()[0]
        plot = PlotFactory(community=self.community, household_count=1, status='residential_habitable')
        survey = Survey.objects.all().order_by('datetime_start')[0]
        next_survey = Survey.objects.all().order_by('datetime_start')[1]

        self.household_structure = HouseholdStructure.objects.get(household__plot=plot, survey=survey)
        self.household_structure_y2 = HouseholdStructure.objects.get(household__plot=plot, survey=next_survey)
        RepresentativeEligibilityFactory(household_structure=self.household_structure)
        RepresentativeEligibilityFactory(household_structure=self.household_structure_y2)

        self.female_dob = date(1989, 10, 10)
        self.female_age_in_years = relativedelta(date.today(), self.female_dob).years
        self.female_first_name = 'ERIKA'
        self.female_last_name = 'WAXON'
        self.female_initials = "EW"

        self.household_member_female_T0 = HouseholdMemberFactory(household_structure=self.household_structure, gender='F', age_in_years=self.female_age_in_years, first_name=self.female_first_name, initials=self.female_initials)
        self.household_member_female_T0.member_status = 'BHS_SCREEN'
        self.household_member_female_T0.save()
        self.assertEqual(self.household_member_female_T0.member_status, 'BHS_SCREEN')
        self.enrollment_checklist_female = EnrollmentChecklistFactory(
            household_member=self.household_member_female_T0,
            gender='F',
            citizen='Yes',
            dob=self.female_dob,
            guardian='No',
            initials=self.household_member_female_T0.initials,
            part_time_resident='Yes')
        self.subject_consent_female = SubjectConsentFactory(household_member=self.household_member_female_T0, study_site=self.study_site, gender='F', dob=self.female_dob, first_name=self.female_first_name, last_name=self.female_last_name, initials=self.female_initials)
        self.registered_subject_female = RegisteredSubject.objects.get(subject_identifier=self.subject_consent_female.subject_identifier)

        enumeration_helper = EnumerationHelper(self.household_structure.household, survey, next_survey)
        self.household_member_female = enumeration_helper.create_member_on_target(self.household_member_female_T0)
        self.appointment_female = Appointment.objects.get(registered_subject=self.registered_subject_female, visit_definition__code='T1')
        self.appointment_female_T0 = Appointment.objects.get(registered_subject=self.registered_subject_female, visit_definition__code='T0')
        self.subject_visit_female_T0 = SubjectVisitFactory(appointment=self.appointment_female_T0, household_member=self.household_member_female_T0)
        self.subject_visit_female = SubjectVisitFactory(appointment=self.appointment_female, household_member=self.household_member_female)

    def test_lastname_and_initials(self):
        CorrectConsentFactory(
            subject_consent=self.subject_consent_female,
            old_last_name=self.female_last_name,
            new_last_name='DIMSTAR',
        )
        self.assertEquals(HouseholdMember.objects.get(id=self.household_member_female_T0.id).initials, 'ED')
        self.assertEquals(EnrollmentChecklist.objects.get(id=self.enrollment_checklist_female.id).initials, 'ED')
        self.assertEquals(SubjectConsent.objects.get(id=self.subject_consent_female.id).initials, 'ED')
        self.assertEquals(SubjectConsent.objects.get(id=self.subject_consent_female.id).last_name, 'DIMSTAR')

    def test_firstname_and_initials(self):
        CorrectConsentFactory(
            subject_consent=self.subject_consent_female,
            old_first_name=self.female_first_name,
            new_first_name='GAME',
        )
        self.assertEquals(HouseholdMember.objects.get(id=self.household_member_female_T0.id).initials, 'GW')
        self.assertEquals(EnrollmentChecklist.objects.get(id=self.enrollment_checklist_female.id).initials, 'GW')
        self.assertEquals(HouseholdMember.objects.get(id=self.household_member_female_T0.id).first_name, 'GAME')
        self.assertEquals(SubjectConsent.objects.get(id=self.subject_consent_female.id).first_name, 'GAME')

#     def test_dob(self):
#         hic = HicEnrollmentFactory(subject_visit=self.subject_visit_female)
#         CorrectConsentFactory(
#             subject_consent=self.subject_consent_female,
#             old_dob=date(1989, 10, 10),
#             new_dob=date(1988, 1, 1),
#         )
#         self.assertEquals(self.household_member_female.age_in_years, 27)
#         self.assertEquals(self.enrollment_checklist_female.dob, date(1988, 1, 1))
#         self.assertEquals(self.subject_consent_female.dob, date(1988, 1, 1))
#         self.assertEquals(hic.dob, date(1988, 1, 1))

    def test_gender(self):
        CorrectConsentFactory(
            subject_consent=self.subject_consent_female,
            old_gender='F',
            new_gender='M',
        )
        self.assertEquals(HouseholdMember.objects.get(id=self.household_member_female_T0.id).gender, 'M')
        self.assertEquals(EnrollmentChecklist.objects.get(id=self.enrollment_checklist_female.id).gender, 'M')
        self.assertEquals(SubjectConsent.objects.get(id=self.subject_consent_female.id).gender, 'M')

    def test_witness(self):
        self.subject_consent_female.witness_name='DIMO'
        self.subject_consent_female.save(update_fields=['witness_name'])
        CorrectConsentFactory(
            subject_consent=self.subject_consent_female,
            old_witness_name='DIMO',
            new_witness_name='BIMO',
        )
        self.assertEquals(SubjectConsent.objects.get(id=self.subject_consent_female.id).witness_name, 'BIMO')
