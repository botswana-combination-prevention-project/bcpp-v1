# from datetime import datetime
# 
# from django.contrib.contenttypes.models import ContentType
# from django.core.exceptions import ValidationError
# from django.test import TestCase
# 
# from edc.core.bhp_content_type_map.classes import ContentTypeMapHelper
# from edc.core.bhp_content_type_map.models import ContentTypeMap
# from edc.core.bhp_variables.tests.factories import StudySpecificFactory, StudySiteFactory
# from edc.map.classes import site_mappers
# from edc.subject.lab_tracker.classes import site_lab_tracker
# from edc.subject.registration.models import RegisteredSubject
# from edc.subject.visit_schedule.models import VisitDefinition
# from edc.subject.visit_schedule.classes import site_visit_schedules
# from edc.subject.rule_groups.classes import site_rule_groups
# from edc.entry_meta_data.models import ScheduledEntryMetaData
# from edc.subject.entry.models import Entry
# from edc.subject.appointment.models import Appointment
# 
# 
# from bhp066.apps.bcpp_household.models import Household, HouseholdStructure
# from bhp066.apps.bcpp_household.tests.factories import PlotFactory
# from bhp066.apps.bcpp_household_member.tests.factories import HouseholdMemberFactory, EnrollmentChecklistFactory
# from bhp066.apps.bcpp_subject.tests.factories import SubjectConsentFactory
# from bhp066.apps.bcpp_subject.tests.factories import (
#     SubjectVisitFactory, HicEnrollmentFactory, SubjectLocatorFactory, ResidencyMobilityFactory, HivResultFactory)
# from bhp066.apps.bcpp_survey.models import Survey
# 
# 
# class TestHicEnrollment(TestCase):
# 
#     def test_p1(self):
#         site_lab_tracker.autodiscover()
#         site_visit_schedules.autodiscover()
#         StudySpecificFactory()
#         study_site = StudySiteFactory()
#         content_type_map_helper = ContentTypeMapHelper()
#         content_type_map_helper.populate()
#         content_type_map_helper.sync()
#         print 'setup the consent catalogue for this BCPP'
#         ContentTypeMap.objects.get(content_type__model__iexact='SubjectConsent')
#         print 'create a new survey'
#         from bhp066.apps.bcpp.app_configuration.classes import BcppAppConfiguration
#         BcppAppConfiguration()
#         site_visit_schedules.build_all()
#         site_rule_groups.autodiscover()
#         print ContentTypeMap.objects.all().count()
# 
#         print 'get a community name from the mapper classes'
#         site_mappers.get_as_list()[0]
#         site_mappers.autodiscover()
#         mapper = site_mappers.get(site_mappers.get_as_list()[0])
#         print 'No. of SURVEY = ' + str(Survey.objects.all().count())
#         plot = PlotFactory(community=mapper().get_map_area())
#         print 'No. of HOUSEHOLDS = ' + str(Household.objects.all().count())
#         Household.objects.get(plot=plot)
#         self.assertEquals(HouseholdStructure.objects.all().count(), 3)
#         self.assertEquals(Survey.objects.all().count(), 3)
#         household_structure = HouseholdStructure.objects.get(survey=Survey.objects.all()[0])
# 
#         household_member = HouseholdMemberFactory(age_in_years=16, household_structure=household_structure)
#         enrollmen_checklist = EnrollmentChecklistFactory(household_member=household_member, initials=household_member.initials, gender=household_member.gender)
#         subject_consent = SubjectConsentFactory(study_site=study_site, citizen='Yes', household_member=household_member, registered_subject=household_member.registered_subject,
#                                                 gender=enrollmen_checklist.gender, dob=enrollmen_checklist.dob, is_literate=enrollmen_checklist.literacy,
#                                                 initials=enrollmen_checklist.initials, guardian_name='MJOLIS, MJOLIS')
#         print subject_consent.subject_identifier
#         print 'get registered subject'
#         RegisteredSubject.objects.get(subject_identifier=subject_consent.subject_identifier)
#         print 'No. of ENTRIES = ' + str(Entry.objects.all().count())
#         content_type = ContentType.objects.get(app_label='bcpp_subject', model='subjectvisit')
#         ContentTypeMap.objects.get(content_type=content_type)
#         self.assertEqual(VisitDefinition.objects.all().count(), 2)
#         visit_definition = VisitDefinition.objects.get(title='T0')  # VisitDefinitionFactory(visit_tracking_content_type_map=content_type_map)
#         print 'No. of Appointments = ' + str(Appointment.objects.all().count())
#         appointment = Appointment.objects.get(visit_definition=visit_definition)
#         print 'No. of ScheduledEntryMetaData before Visit = ' + str(ScheduledEntryMetaData.objects.all().count())
#         subject_visit = SubjectVisitFactory(household_member=household_member, appointment=appointment)
#         print 'No. of ScheduledEntryMetaData after Visit = ' + str(ScheduledEntryMetaData.objects.all().count())
#         # Try to create an HicEnrollment form, should fail as no ResidencyMobility form.
#         self.assertRaises(ValidationError, lambda: HicEnrollmentFactory(subject_visit=subject_visit, dob=subject_consent.dob, consent_datetime=subject_consent.consent_datetime))
#         # Create a RecidencyMobility form
#         recidency_mobility = ResidencyMobilityFactory(subject_visit=subject_visit, permanent_resident='Yes', intend_residency='No')
#         # Try to create an HicEnrollment form, should fail as no HivResult form.
#         self.assertRaises(ValidationError, lambda: HicEnrollmentFactory(subject_visit=subject_visit, dob=subject_consent.dob, consent_datetime=subject_consent.consent_datetime))
#         # Create an HivResult form
#         hiv_result = HivResultFactory(subject_visit=subject_visit, hiv_result='NEG')
#         # Try to create an HicEnrollment form, should fail as no SubjectLocator form.
#         self.assertRaises(ValidationError, lambda: HicEnrollmentFactory(subject_visit=subject_visit, dob=subject_consent.dob, consent_datetime=subject_consent.consent_datetime))
#         # Create an SubjectLocator form
#         locator = SubjectLocatorFactory(subject_visit=subject_visit, may_follow_up='Yes', subject_cell='72738888', subject_cell_alt='72738877', subject_phone='5483790')
#         # Try to create an HicEnrollment form, should pass.
#         HicEnrollmentFactory(subject_visit=subject_visit, dob=subject_consent.dob, consent_datetime=subject_consent.consent_datetime)
#         # Try change dob or consent_datetime in subject consent
#         subject_consent.dob = datetime(1970, 10, 10)
#         self.assertRaises(ValidationError, lambda: subject_consent.save())
#         subject_consent.consent_datetime = datetime.today()
#         self.assertRaises(ValidationError, lambda: subject_consent.save())
#         # try change HivResult
#         hiv_result.hiv_result = 'POS'
#         self.assertRaises(ValidationError, lambda: hiv_result.save())
#         # try change residency
#         recidency_mobility.intend_residency = 'Yes'
#         self.assertRaises(ValidationError, lambda: recidency_mobility.save())
#         # try remove all contact numbers in locator
#         locator.may_follow_up = ''
#         locator.subject_cell = ''
#         locator.subject_cell_alt = ''
#         locator.subject_phone = ''
#         self.assertRaises(ValidationError, lambda: locator.save())
