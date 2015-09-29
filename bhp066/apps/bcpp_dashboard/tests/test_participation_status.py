# from datetime import datetime, timedelta, date
# from dateutil.relativedelta import relativedelta
# 
# from django.test import TestCase
# from django.db.models import signals
# 
# from edc.core.bhp_variables.tests.factories import StudySiteFactory
# from edc.lab.lab_profile.classes import site_lab_profiles
# from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
# from edc.map.classes import Mapper, site_mappers
# from edc.subject.appointment_helper.models import prepare_appointments_on_post_save
# from edc.subject.lab_tracker.classes import site_lab_tracker
# 
# from bhp066.apps.bcpp.app_configuration.classes import BcppAppConfiguration
# from bhp066.apps.bcpp_household.models import HouseholdStructure, Household
# from bhp066.apps.bcpp_household.tests.factories import PlotFactory
# from bhp066.apps.bcpp_household_member.models import SubjectAbsentee, SubjectAbsenteeEntry
# from bhp066.apps.bcpp_household_member.tests.factories import EnrollmentChecklistFactory, HouseholdMemberFactory
# from bhp066.apps.bcpp_lab.lab_profiles import BcppSubjectProfile
# from bhp066.apps.bcpp_subject.models import SubjectConsent
# from bhp066.apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule
# from bhp066.apps.bcpp_survey.models import Survey
# 
# # from ..views.participation import update_member_status
# 
# 
# class TestPlotMapper(Mapper):
#     map_area = 'test_community4'
#     map_code = '092'
#     regions = []
#     sections = []
#     landmarks = []
#     gps_center_lat = -25.033194
#     gps_center_lon = 25.747139
#     radius = 5.5
#     location_boundary = ()
# 
# site_mappers.register(TestPlotMapper)
# 
# 
# class TestParticipationStatus(TestCase):
# 
#     def setUp(self):
#         try:
#             site_lab_profiles.register(BcppSubjectProfile())
#         except AlreadyRegisteredLabProfile:
#             pass
#         BcppAppConfiguration()
#         site_lab_tracker.autodiscover()
#         BcppSubjectVisitSchedule().build()
# 
#         self.survey1 = Survey.objects.get(survey_name='BCPP Year 1')  # see app_configuration
#         plot = PlotFactory(community='test_community4', household_count=1, status='residential_habitable')
#         household = Household.objects.get(plot=plot)
#         self.household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)
# 
#     def test_new_member_status_is_not_reported(self):
#         """Assert new eligible member by default is NOT_REPORTED."""
#         household_member = HouseholdMemberFactory(
#             household_structure=self.household_structure,
#             age_in_years=25)
#         self.assertEqual(household_member.member_status, 'NOT_REPORTED')
# 
#     def test_new_member_status_is_not_eligible_by_age1(self):
#         """Assert new ineligible member by default is NOT_ELIGIBLE."""
#         household_member = HouseholdMemberFactory(
#             household_structure=self.household_structure,
#             age_in_years=2)
#         self.assertEqual(household_member.member_status, 'NOT_ELIGIBLE')
# 
#     def test_new_member_status_is_not_eligible_by_age2(self):
#         """Assert new ineligible (bhs), eligible htc member by default is NOT_ELIGIBLE, NOT_REPORTED."""
#         household_member = HouseholdMemberFactory(
#             household_structure=self.household_structure,
#             age_in_years=65)
#         self.assertEqual(household_member.member_status, 'NOT_ELIGIBLE')
# 
#     def test_change_absent(self):
#         """Assert when new member changed to absent a subject_absentee instance is created."""
#         household_member = HouseholdMemberFactory(
#             household_structure=self.household_structure,
#             age_in_years=50)
#         self.assertEqual(SubjectAbsentee.objects.filter(household_member=household_member).count(), 0)
#         self.assertNotEqual('ABSENT', household_member.member_status)
#         new_status, eligible_subject, changed = update_member_status(household_member, 'ABSENT')
#         self.assertEqual('ABSENT', new_status)
#         self.assertEqual(eligible_subject, False)
#         self.assertEqual(changed, True)
#         self.assertEqual(SubjectAbsentee.objects.filter(household_member=household_member).count(), 1)
# 
#     def test_change_to_absent_and_back1(self):
#         """new member changed from absent and deletes a subject_absentee instance if no entries."""
#         household_member = HouseholdMemberFactory(
#             household_structure=self.household_structure,
#             age_in_years=50,
#             present_today='No',  # on day of survey
#             study_resident='Yes')
#         self.assertEqual(SubjectAbsentee.objects.filter(household_member=household_member).count(), 0)
#         update_member_status(household_member, "ABSENT")
#         subject_absentee = SubjectAbsentee.objects.filter(household_member=household_member)
#         self.assertEqual(SubjectAbsenteeEntry.objects.filter(subject_absentee=subject_absentee).count(), 0)
#         new_member_status = update_member_status(household_member, 'NOT_REPORTED')
#         self.assertEqual('NOT_REPORTED', new_member_status)
#         self.assertEqual(SubjectAbsentee.objects.filter(household_member=household_member).count(), 0)
# 
#     def test_change_to_absent_and_back2(self):
#         """new member changed from absent and does not delete the subject_absentee instance with entries."""
#         household_member = HouseholdMemberFactory(
#             household_structure=self.household_structure,
#             age_in_years=50,
#             present_today='No',  # on day of survey
#             study_resident='Yes')
#         self.assertTrue(household_member.eligible_member)
#         self.assertFalse(household_member.eligible_subject)
#         self.assertEqual('NOT_REPORTED', household_member.member_status)
#         self.assertEqual(SubjectAbsentee.objects.filter(household_member=household_member).count(), 0)
#         update_member_status(household_member, 'ABSENT')
#         self.assertEqual('ABSENT', household_member.member_status)
#         subject_absentee = SubjectAbsentee.objects.filter(household_member=household_member)
#         self.assertEqual(SubjectAbsenteeEntry.objects.filter(subject_absentee=subject_absentee).count(), 0)
#         SubjectAbsenteeEntry.objects.create(
#             subject_absentee=SubjectAbsentee.objects.get(household_member=household_member),
#             report_datetime=datetime.today(),
#             reason='reason',
#             next_appt_datetime=datetime.today() + timedelta(days=10),
#             next_appt_datetime_source='erik')
#         self.assertEqual(SubjectAbsenteeEntry.objects.filter(subject_absentee=subject_absentee).count(), 1)
#         update_member_status(household_member, 'NOT_REPORTED')
#         self.assertEqual('NOT_REPORTED', household_member.member_status)
#         self.assertEqual(household_member.eligible_subject, False)
#         self.assertEqual(SubjectAbsentee.objects.filter(household_member=household_member).count(), 1)
# 
#     def test_change_from_research1(self):
#         """change from research to something else and clear eligible_subject if true."""
#         household_member = HouseholdMemberFactory(
#             household_structure=self.household_structure,
#             gender='M',
#             age_in_years=50)
#         EnrollmentChecklistFactory(
#             household_member=household_member,
#             gender='M',
#             dob=date.today() - relativedelta(years=50),
#             initials=household_member.initials,
#             part_time_resident='Yes')
#         household_member.member_status = 'RESEARCH'
#         household_member.save()
#         self.assertTrue(household_member.eligible_subject)
#         cleaned_data = {'status': 'REFUSED'}
#         update_member_status(household_member, cleaned_data)
#         self.assertEqual(household_member.member_status, 'REFUSED')
# 
#     def test_change_from_research2(self):
#         """change from research with consent to something else, should not clear eligible_subject and not change."""
#         signals.post_save.disconnect(prepare_appointments_on_post_save, weak=False, dispatch_uid='prepare_appointments_on_post_save')
#         household_member = HouseholdMemberFactory(
#             household_structure=self.household_structure,
#             gender='M',
#             age_in_years=50,
#             study_resident='Yes')
#         EnrollmentChecklistFactory(
#             household_member=household_member,
#             gender='M',
#             dob=date.today() - relativedelta(years=50),
#             initials=household_member.initials,
#             part_time_resident='Yes')
#         household_member.member_status = 'RESEARCH'
#         household_member.save()
#         self.assertTrue(household_member.eligible_subject)
# 
#         SubjectConsent.objects.create(  # TODO: replace with factory
#             household_member=household_member,
#             registered_subject=household_member.registered_subject,
#             survey=household_member.household_structure.survey,
#             identity='111111111',
#             identity_type='OMANG',
#             gender='M',
#             first_name='ERIK',
#             last_name='ERIK',
#             initials='EE',
#             study_site=StudySiteFactory(),
#             consent_datetime=datetime.today(),
#             may_store_samples='Yes',
#             is_incarcerated='No',
#             is_literate='Yes',
#         )
#         cleaned_data = {'status': 'REFUSED'}
#         update_member_status(household_member, cleaned_data)
#         self.assertTrue(household_member.eligible_subject)
#         self.assertEqual(household_member.member_status, 'RESEARCH')
