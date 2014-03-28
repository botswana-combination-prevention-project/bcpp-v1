from datetime import datetime

from django.test import TestCase

from edc.core.bhp_content_type_map.classes import ContentTypeMapHelper
from edc.map.classes import site_mappers
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.registration.models import RegisteredSubject

from apps.bcpp_household.models import Household, HouseholdStructure
from apps.bcpp_household.tests.factories import PlotFactory
from apps.bcpp_household_member.tests.factories import HouseholdMemberFactory
from apps.bcpp_subject.tests.factories import SubjectConsentFactory
from apps.bcpp_survey.tests.factories import SurveyFactory


class ConsentHistoryTests(TestCase):

    def test_p1(self):
        site_lab_tracker.autodiscover()
        site_mappers.autodiscover()
        content_type_map_helper = ContentTypeMapHelper()
        content_type_map_helper.populate()
        content_type_map_helper.sync()
        print 'get a community name from the mapper classes'
        community = site_mappers.get_as_list()[0]
        print 'create a new survey'
        self.assertEquals(RegisteredSubject.objects.all().count(), 0)
        self.assertEquals(Household.objects.all().count(), 0)
        self.assertEquals(HouseholdStructure.objects.all().count(), 0)
        survey1 = SurveyFactory(datetime_start=datetime(2013, 07, 01), datetime_end=datetime(2013,12,01))
        survey2 = SurveyFactory(datetime_start=datetime(2014, 01, 01), datetime_end=datetime(2014,07,01))
        survey3 = SurveyFactory(datetime_start=datetime(2015, 01, 01), datetime_end=datetime(2015,07,01))
        print('get site mappers')
        site_mappers.autodiscover()
        print('get one mapper')
        mapper = site_mappers.get(site_mappers.get_as_list()[0])
        print('mapper is {0}'.format(mapper().get_map_area()))
        print('Create a plot, (note plot creates a HH if None exist)')
        plot = PlotFactory(community=mapper().get_map_area())
        household = Household.objects.get(plot=plot)
        self.assertEquals(Household.objects.all().count(), 1)
        print 'assert hh structure created'
        self.assertEquals(HouseholdStructure.objects.all().count(), 3)  # 3 surveys for each HH = 3 x 1 = 3
        household_structure = HouseholdStructure.objects.get(survey=survey1)
        print 'create HH members for this survey and HH {0}'.format(household)
        hm1 = HouseholdMemberFactory(household_structure=household_structure)
        self.assertEquals(RegisteredSubject.objects.all().count(), 1)
        print hm1.registered_subject.pk
        hm2 = HouseholdMemberFactory(household_structure=household_structure)
        self.assertEquals(RegisteredSubject.objects.all().count(), 2)
        print hm2.registered_subject.pk
        hm3 = HouseholdMemberFactory(household_structure=household_structure)
        self.assertEquals(RegisteredSubject.objects.all().count(), 3)
        print hm2.registered_subject.pk
        print 'confirm RS created when HM created'
        self.assertEquals(RegisteredSubject.objects.all().count(), 3)
        print 'Consent each HM'
        SubjectConsentFactory(first_name='THING1', survey=survey1, household_member=hm1, registered_subject=hm1.registered_subject)
        SubjectConsentFactory(first_name='THING2', survey=survey1, household_member=hm2, registered_subject=hm1.registered_subject)
        subject_consent = SubjectConsentFactory(first_name='THING3', survey=survey1, household_member=hm3, registered_subject=hm1.registered_subject)

#         print 'assert has consent history methods'
#         self.assertTrue('get_consent_history_model' in dir(subject_consent))
#         self.assertTrue('update_consent_history' in dir(subject_consent))
#         self.assertTrue('delete_consent_history' in dir(subject_consent))
#         print 'confirm RS created'
#         self.assertEquals(RegisteredSubject.objects.all().count(), 3)
#         self.assertEquals(RegisteredSubject.objects.filter(first_name=subject_consent.first_name, dob=subject_consent.dob, initials=subject_consent.initials).count(), 1)
#         print 'assert get_consent_history_model returns a model of base class BaseConsentHistory'
#         history_model = subject_consent.get_consent_history_model()
#         self.assertIsNotNone(subject_consent.get_consent_history_model())
#         self.assertTrue(issubclass(subject_consent.get_consent_history_model(), BaseConsentHistory))
#         print 'assert consent history now includes consent for {0}'.format(subject_consent)
#         self.assertEquals(history_model.objects.filter(registered_subject=subject_consent.registered_subject).count(), 1)
#         subject_consent_history = history_model.objects.get(registered_subject=subject_consent.registered_subject, consent_pk=subject_consent.pk)
#         self.assertEqual(subject_consent.consent_datetime, subject_consent_history.consent_datetime)
#         print 'update consent for {0}'.format(subject_consent)
#         subject_consent.consent_datetime = datetime.today()
#         subject_consent.save()
#         print 'assert history updated for {0}'.format(subject_consent)
#         subject_consent_history = history_model.objects.get(registered_subject=subject_consent.registered_subject, consent_pk=subject_consent.pk)
#         self.assertEqual(subject_consent.consent_datetime, subject_consent_history.consent_datetime)
#         print 'delete consent for {0}'.format(subject_consent)
#         subject_consent.delete()
#         print 'assert history update for {0}'.format(subject_consent)
#         self.assertEqual(history_model.objects.filter(registered_subject=subject_consent.registered_subject, consent_pk=subject_consent.pk).count(), 0)
#         self.assertEqual(history_model.objects.all().count(), 3)
