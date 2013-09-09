# from django.test import TestCase
# from bhp_entry.models import ScheduledEntryBucket
# from bhp_entry.classes import ScheduledEntry
# from datetime import datetime, date, timedelta
# from bhp_lab_tracker.classes import lab_tracker
# from bhp_variables.models import StudySpecific, StudySite
# from bhp_variables.tests.factories import StudySpecificFactory, StudySiteFactory
# from bhp_registration.models import RegisteredSubject
# from bhp_consent.tests.factories import ConsentCatalogueFactory
# from bhp_appointment.tests.factories import ConfigurationFactory
# from bhp_visit.tests.factories import MembershipFormFactory, ScheduleGroupFactory, VisitDefinitionFactory
# from bhp_content_type_map.classes import ContentTypeMapHelper
# from bhp_content_type_map.models import ContentTypeMap
# from bhp_base_test.tests.factories import TestConsentFactory, TestBaseOffStudyFactory
# from bhp_base_test.models import TestConsent, TestRegistration, TestVisit
# 
# 
# class ScheduledEntryMethodsTests(TestCase):
#     
#     app_label = 'bhp_base_test'
#     consent_catalogue_name = 'v1'
# 
#     def test_show_scheduled_entries(self):
#         lab_tracker.autodiscover()
#         StudySpecificFactory()
#         study_site = StudySiteFactory()
#         ConfigurationFactory()
#         content_type_map_helper = ContentTypeMapHelper()
#         content_type_map_helper.populate()
#         content_type_map_helper.sync()
#         print 'setup the consent catalogue for app {0}'.format(self.app_label)
#         content_type_map = ContentTypeMap.objects.get(content_type__model=TestConsent._meta.object_name.lower())
#         consent_catalogue = ConsentCatalogueFactory(name=self.consent_catalogue_name, content_type_map=content_type_map)
#         consent_catalogue.add_for_app = self.app_label
#         consent_catalogue.save()
# 
#         print 'setup bhp_visit'
#         content_type_map = ContentTypeMap.objects.get(content_type__model=TestRegistration._meta.object_name.lower())
#         membership_form = MembershipFormFactory(content_type_map=content_type_map)
#         schedule_group = ScheduleGroupFactory(membership_form=membership_form, group_name='Registration', grouping_key='ELIGIBILITY')
#         visit_definition = VisitDefinitionFactory(code='1000', title='Registration', grouping='subject')
#         visit_definition.schedule_group.add(schedule_group)
# 
#         print 'consent a subject (2 days ago)'
#         test_consent = TestConsentFactory(study_site=study_site, consent_datetime=datetime.today() - timedelta(days=2))
#         print test_consent.subject_identifier
#         print 'get maternal registered subject'
#         registered_subject = RegisteredSubject.objects.get(subject_identifier=test_consent.subject_identifier)
#         print 'take subject off study (1 day ago)'
#         test_off_study = TestBaseOffStudyFactory(registered_subject=registered_subject, offstudy_date=date.today() - timedelta(days=1))
#         print 'Off study: {0}'.format(test_off_study)
