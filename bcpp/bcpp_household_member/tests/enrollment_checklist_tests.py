from datetime import datetime, date

from django.test import TestCase
from django.core.exceptions import ValidationError

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc_map.classes import Mapper, site_mappers
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.registration.models import RegisteredSubject
from edc_constants.constants import NOT_APPLICABLE

from bhp066.apps.bcpp.app_configuration.classes import BcppAppConfiguration
from bhp066.apps.bcpp_household.models import Household, HouseholdStructure
from bhp066.apps.bcpp_household.tests.factories import PlotFactory
from bhp066.apps.bcpp_household_member.models import EnrollmentLoss
from bhp066.apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from bhp066.apps.bcpp_subject.tests.factories import SubjectConsentFactory
from bhp066.apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule
from bhp066.apps.bcpp_survey.models import Survey


class TestPlotMapper(Mapper):
    map_area = 'test_community4'
    map_code = '092'
    regions = []
    sections = []
    landmarks = []
    gps_center_lat = -25.033194
    gps_center_lon = 25.747139
    radius = 5.5
    location_boundary = ()
site_mappers.register(TestPlotMapper)


class EnrollmentChecklistTests(TestCase):
    def __init__(self, *args, **kwargs):
        self.household_member = None
        self.subject_consent = None
        self.enrollment_checklist = None
        self.registered_subject = None
        self.study_site = None
        super(EnrollmentChecklistTests, self).__init__(*args, **kwargs)

    def setUp(self):
        try:
            site_lab_profiles.register(BcppSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        BcppAppConfiguration()
        site_lab_tracker.autodiscover()
        BcppSubjectVisitSchedule().build()

        self.survey1 = Survey.objects.get(survey_name='BCPP Year 1')  # see app_configuration
        plot = PlotFactory(community='test_community3', household_count=1, status='residential_habitable')
        household = Household.objects.get(plot=plot)
        self.household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)

    def test_household_member1(self):
#         self.assertTrue(self.household_member.is_eligible)

        #Create with a < 16 DOB, should make member ineligible
        #enrollment_checklist.dob = datetime(2000,01,01)
        #enrollment_checklist.save()
        #Assert household member ineligible and put it back to its original value
        #self.assertEqual(household_member.member_status, 'NOT_ELIGIBLE')
        #enrollment_checklist.dob = datetime(1994,10,10)
        #household_member.member_status = 'BHS'
        #enrollment_checklist.save()
        #Edit enrollment checklist to make them a minor without guardian available
        self.enrollment_checklist.guardian = 'No'
        self.enrollment_checklist.dob = datetime(1998,01,01).date()
        #Assert household member ineligible and put back to normal
        self.household_member.age_in_years = 16
        self.enrollment_checklist.save()
        #self.assertEqual(self.household_member.member_status, 'NOT_ELIGIBLE')
        self.assertFalse(self.household_member.eligible_subject)
        self.assertEqual(EnrollmentLoss.objects.all().count(),1)
        EnrollmentLoss.objects.get(household_member=self.household_member).delete()
        self.enrollment_checklist.dob = datetime(1994,01,10).date()
        self.household_member.age_in_years = 20
        #self.household_member.member_status = 'BHS'
        self.enrollment_checklist.guardian = 'Yes'
        self.enrollment_checklist.save()
        #Edit enrollment checklist to say they dont have identity
        self.enrollment_checklist.has_identity = 'No'
        self.enrollment_checklist.save()
        #Assert household member ineligible
        #self.assertEqual(self.household_member.member_status, 'NOT_ELIGIBLE')
        self.assertFalse(self.household_member.eligible_subject)
        self.assertEqual(EnrollmentLoss.objects.all().count(),1)
        EnrollmentLoss.objects.get(household_member=self.household_member).delete()
        self.enrollment_checklist.has_identity = 'Yes'
        self.enrollment_checklist.save()
        #self.household_member.member_status = 'BHS'
        #Edit enrollment checklist to say they are a non-citizen married to citizen with valid marriage certificate.
        self.enrollment_checklist.citizen = 'No'
        self.enrollment_checklist.legal_marriage = 'Yes'
        self.enrollment_checklist.marriage_certificate = 'Yes'
        self.enrollment_checklist.save()
        #Assert household member is eligible
        #self.assertEqual(self.household_member.member_status, 'BHS')
        self.assertTrue(self.household_member.eligible_subject)
        #self.assertEqual(EnrollmentLoss.objects.all().count(),1)
        #EnrollmentLoss.objects.get(household_member=household_member).delete()
        self.enrollment_checklist.citizen = 'Yes'
        self.enrollment_checklist.legal_marriage = NOT_APPLICABLE
        self.enrollment_checklist.marriage_certificate = NOT_APPLICABLE
        self.enrollment_checklist.save()
        #self.household_member.member_status = 'BHS'
        #Edit enrollment checklist to say that they are part time residents
        self.enrollment_checklist.part_time_resident = 'No'
        self.enrollment_checklist.save()
        #Assert household member ineligible
        #self.assertEqual(self.household_member.member_status, 'NOT_ELIGIBLE')
        self.assertFalse(self.household_member.eligible_subject)
        self.assertEqual(EnrollmentLoss.objects.all().count(),1)
        EnrollmentLoss.objects.get(household_member=self.household_member).delete()
        self.enrollment_checklist.part_time_resident = 'Yes'
        self.enrollment_checklist.save()
        self.household_member.member_status = 'BHS'
        #Edit enrollment to say that that they are an illitrate without a litirate witness available
        self.enrollment_checklist.literacy = 'No'
        self.enrollment_checklist.save()
        #Assert household member ineligible
        #self.assertEqual(self.household_member.member_status, 'NOT_ELIGIBLE')
        self.assertFalse(self.household_member.eligible_subject)
        self.assertEqual(EnrollmentLoss.objects.all().count(),1)
        EnrollmentLoss.objects.get(household_member=self.household_member).delete()
        self.enrollment_checklist.literacy = 'Yes'
        self.enrollment_checklist.save()
        #self.household_member.member_status = 'BHS'
        #Edit enrollment checklist to say they are not a household resident
        self.enrollment_checklist.household_residency = 'No'
        self.enrollment_checklist.save()
        #Assert household member ineligible
        #self.assertEqual(self.household_member.member_status, 'NOT_ELIGIBLE')
        self.assertFalse(self.household_member.eligible_subject)
        self.assertEqual(EnrollmentLoss.objects.all().count(),1)
        EnrollmentLoss.objects.get(household_member=self.household_member).delete()
        self.enrollment_checklist.household_residency = 'Yes'
        self.enrollment_checklist.save()
        #self.household_member.member_status = 'BHS'

        self.enrollment_checklist.dob = date(1997,10,10)
        self.enrollment_checklist.save()
        self.subject_consent = SubjectConsentFactory(dob=self.enrollment_checklist.dob,study_site=self.study_site, citizen='Yes',initials=self.enrollment_checklist.initials,
                                                     household_member=self.household_member, registered_subject=self.household_member.registered_subject,
                                                     guardian_name="THUSO, THUSO")
        self.registered_subject = RegisteredSubject.objects.get(subject_identifier=self.subject_consent.subject_identifier)
        #Assert that you cannot save enrollment checklist after consent entered

        #Attempt to change dob in consent thats used in enrollment checklist.
        self.subject_consent.dob = datetime(1971,01,01).date()
        #Assert consent for throwing error
        self.assertRaises(ValidationError, lambda: self.subject_consent.save())
        self.subject_consent.dob = self.enrollment_checklist.dob
        #Attempt to change citizenship in consent thats used in enrollment checklist
        self.subject_consent.citizen = 'No'
        #Assert consent for throwing error
        self.assertRaises(ValidationError, lambda: self.subject_consent.save())
        self.subject_consent.citizen = 'Yes'
        #Attempt to change Initials in consent to whats used in checklist
        self.subject_consent.initials = 'OO'
        #Assert consent throws error
        self.assertRaises(ValidationError, lambda: self.subject_consent.save())
        self.subject_consent.initials = self.enrollment_checklist.initials
#         #Attempt to guardian status in consents to wats in enrollment checklist
#         self.enrollment_checklist.guardian = 'Yes'
#         #Assert consent throws errror
#         self.assertRaises(TypeError, lambda: self.subject_consent.save())
#         self.enrollment_checklist.guardian = self.enrollment_checklist.initials
        #Attempt to change gender in consent to whats in enrollment checklist
        self.subject_consent.gender = 'F'
        #Assert consent throws error
        self.assertRaises(ValidationError, lambda: self.subject_consent.save())
        self.subject_consent.gender = 'M'
        #Attempt to change marriage status of non citizen to whats different from checklist
        self.subject_consent.legal_marriage = 'Yes'
        self.subject_consent.marriage_certificate = 'Yes'
        #No consent error
        self.subject_consent.save()