from datetime import datetime, timedelta, date

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.core.exceptions import ValidationError

from edc.core.bhp_content_type_map.classes import ContentTypeMapHelper
from edc.core.bhp_content_type_map.models import ContentTypeMap
from edc.core.bhp_variables.tests.factories import StudySpecificFactory, StudySiteFactory
from edc.map.classes import site_mappers
from edc.subject.appointment.tests.factories import ConfigurationFactory
from edc.subject.consent.tests.factories import ConsentCatalogueFactory
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.registration.models import RegisteredSubject
from edc.subject.visit_schedule.classes import site_visit_schedules
from edc.subject.rule_groups.classes import site_rule_groups


from apps.bcpp_household.models import Household, HouseholdStructure
from apps.bcpp_household.tests.factories import PlotFactory
from apps.bcpp_household_member.models import Loss, HouseholdMember
from apps.bcpp_household_member.tests.factories import HouseholdMemberFactory, EnrolmentChecklistFactory
from apps.bcpp_subject.tests.factories import SubjectConsentFactory
from apps.bcpp_survey.models import Survey


class EnrollmentChecklistTests(TestCase):
    def __init__(self, *args, **kwargs):
        self.household_member = None
        self.subject_consent = None
        self.enrollment_checklist = None
        self.registered_subject = None
        self.study_site = None
        super(EnrollmentChecklistTests, self).__init__(*args, **kwargs)

    def setUp(self):
        site_lab_tracker.autodiscover()
        site_visit_schedules.autodiscover()
        StudySpecificFactory()
        study_site = StudySiteFactory()
        ConfigurationFactory()
        content_type_map_helper = ContentTypeMapHelper()
        content_type_map_helper.populate()
        content_type_map_helper.sync()  
        print 'setup the consent catalogue for this BCPP'
        content_type_map = ContentTypeMap.objects.get(content_type__model__iexact='SubjectConsent')
        print 'create a new survey'
        from apps.bcpp.app_configuration.classes import BcppAppConfiguration
        BcppAppConfiguration()
        site_visit_schedules.build_all()
        site_rule_groups.autodiscover()
        print ContentTypeMap.objects.all().count()
        consent_catalogue = ConsentCatalogueFactory(name='bcpp year 0', content_type_map=content_type_map)
        consent_catalogue.add_for_app = 'bcpp_subject'
        consent_catalogue.save()

        print 'get a community name from the mapper classes'
        community = site_mappers.get_as_list()[0]
        site_mappers.autodiscover()
        mapper = site_mappers.get(site_mappers.get_as_list()[0])
        print 'No. of SURVEY = '+str(Survey.objects.all().count()) 
        plot = PlotFactory(community=mapper().get_map_area())
        print 'No. of HOUSEHOLDS = '+str(Household.objects.all().count())
        household = Household.objects.get(plot=plot)
        self.assertEquals(HouseholdStructure.objects.all().count(), 3)
        self.assertEquals(Survey.objects.all().count(), 3)
        household_structure = HouseholdStructure.objects.get(survey=Survey.objects.all()[0])

        self.household_member = HouseholdMemberFactory(member_status='BHS', age_in_years=16, household_structure=household_structure)
#         subject_consent = SubjectConsentFactory(study_site=study_site, citizen='Yes', household_member=self.household_member, registered_subject=self.household_member.registered_subject)
#         print subject_consent.subject_identifier
#         print 'get registered subject'
#         registered_subject = RegisteredSubject.objects.get(subject_identifier=subject_consent.subject_identifier)

    def test_checklist_household_member(self):
        #Create a proper enrollment checklist, confirm that householdmeber is eligible.
        self.assertEqual(HouseholdMember.objects.all().count(), 1)
        #self.household_member = HouseholdMember.objects.all()[0]
        self.enrollment_checklist = EnrolmentChecklistFactory(household_member=self.household_member, initials=self.household_member.initials, gender=self.household_member.gender)
        #self.assertEqual(self.household_member.member_status, 'BHS')
        self.assertTrue(self.household_member.eligible_subject)
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
        self.assertEqual(Loss.objects.all().count(),1)
        Loss.objects.get(household_member=self.household_member).delete()
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
        self.assertEqual(Loss.objects.all().count(),1)
        Loss.objects.get(household_member=self.household_member).delete()
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
        #self.assertEqual(Loss.objects.all().count(),1)
        #Loss.objects.get(household_member=household_member).delete()
        self.enrollment_checklist.citizen = 'Yes'
        self.enrollment_checklist.legal_marriage = 'N/A'
        self.enrollment_checklist.marriage_certificate = 'N/A'
        self.enrollment_checklist.save()
        #self.household_member.member_status = 'BHS'
        #Edit enrollment checklist to say that they are part time residents
        self.enrollment_checklist.part_time_resident = 'No'
        self.enrollment_checklist.save()
        #Assert household member ineligible
        #self.assertEqual(self.household_member.member_status, 'NOT_ELIGIBLE')
        self.assertFalse(self.household_member.eligible_subject)
        self.assertEqual(Loss.objects.all().count(),1)
        Loss.objects.get(household_member=self.household_member).delete()
        self.enrollment_checklist.part_time_resident = 'Yes'
        self.enrollment_checklist.save()
        self.household_member.member_status = 'BHS'
        #Edit enrollment to say that that they are an illitrate without a litirate witness available
        self.enrollment_checklist.literacy = 'No'
        self.enrollment_checklist.save()
        #Assert household member ineligible
        #self.assertEqual(self.household_member.member_status, 'NOT_ELIGIBLE')
        self.assertFalse(self.household_member.eligible_subject)
        self.assertEqual(Loss.objects.all().count(),1)
        Loss.objects.get(household_member=self.household_member).delete()
        self.enrollment_checklist.literacy = 'Yes'
        self.enrollment_checklist.save()
        #self.household_member.member_status = 'BHS'
        #Edit enrollment checklist to say they are not a household resident
        self.enrollment_checklist.household_residency = 'No'
        self.enrollment_checklist.save()
        #Assert household member ineligible
        #self.assertEqual(self.household_member.member_status, 'NOT_ELIGIBLE')
        self.assertFalse(self.household_member.eligible_subject)
        self.assertEqual(Loss.objects.all().count(),1)
        Loss.objects.get(household_member=self.household_member).delete()
        self.enrollment_checklist.household_residency = 'Yes'
        self.enrollment_checklist.save()
        #self.household_member.member_status = 'BHS'

        self.enrollment_checklist.dob = date(1997,10,10)
        self.enrollment_checklist.save()
        self.subject_consent = SubjectConsentFactory(dob=self.enrollment_checklist.dob,study_site=self.study_site, citizen='Yes',initials=self.enrollment_checklist.initials,
                                                     household_member=self.household_member, registered_subject=self.household_member.registered_subject,
                                                     guardian_name="THUSO, THUSO")
        print self.subject_consent.subject_identifier
        print 'get registered subject'
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
        #Attempt to change gender in consent to whats in enrolment checklist
        self.subject_consent.gender = 'F'
        #Assert consent throws error
        self.assertRaises(ValidationError, lambda: self.subject_consent.save())
        self.subject_consent.gender = 'M'
        #Attempt to change marriage status of non citizen to whats different from checklist
        self.subject_consent.legal_marriage = 'Yes'
        self.subject_consent.marriage_certificate = 'Yes'
        #No consent error
        self.subject_consent.save()