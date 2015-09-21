from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from django.test import TestCase

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.map.classes import site_mappers
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.registration.models import RegisteredSubject
from edc.core.bhp_variables.models import StudySite

from bhp066.apps.bcpp.app_configuration.classes import BcppAppConfiguration
from bhp066.apps.bcpp_household.models import Household, HouseholdStructure, Plot
from bhp066.apps.bcpp_household.tests.factories import PlotFactory, RepresentativeEligibilityFactory
from bhp066.apps.bcpp_household_member.tests.factories import HouseholdMemberFactory, EnrollmentChecklistFactory
from bhp066.apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from bhp066.apps.bcpp_subject.tests.factories import SubjectConsentFactory
from bhp066.apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule
from bhp066.apps.bcpp_survey.models import Survey


class TestConsentHistory(TestCase):

    app_label = 'bcpp_subject'
    community = None

    def startup(self):
        try:
            site_lab_profiles.register(BcppSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass

        BcppAppConfiguration()
        site_lab_tracker.autodiscover()
        BcppSubjectVisitSchedule().build()
        site_mappers.autodiscover()
        self.study_site = StudySite.objects.get(site_code=site_mappers.get_current_mapper().map_code)

    def test_p1(self):
        self.startup()
        print 'get a community name from the mapper classes'
        community = site_mappers.get_current_mapper().map_area
        print 'create a new survey'
        self.assertEquals(RegisteredSubject.objects.all().count(), 0)
        self.assertEquals(Household.objects.all().count(), 0)
        self.assertEquals(HouseholdStructure.objects.all().count(), 0)
        self.assertEquals(Plot.objects.all().count(), 0)
        survey1, survey2, survey3 = [survey for survey in Survey.objects.all()]
        print('get site mappers')
        site_mappers.autodiscover()
        print('get one mapper')
        mapper = site_mappers.get(site_mappers.get_as_list()[0])
        print('mapper is {0}'.format(mapper().get_map_area()))
        print('Create a plot, (note plot creates a HH if None exist)')
        plot = PlotFactory(community=community, household_count=1, status='residential_habitable')
        print plot
        household = Household.objects.get(plot=plot)
        print [h.household for h in HouseholdStructure.objects.all()]
        print [h.survey for h in HouseholdStructure.objects.all()]
        self.assertEquals(Household.objects.all().count(), 1)
        print 'assert hh structure created'
        self.assertEquals(HouseholdStructure.objects.all().count(), 3)  # 3 surveys for each HH = 3 x 1 = 3
        household_structure = HouseholdStructure.objects.get(survey=survey1)
        print 'add RepresentativeEligibility'
        RepresentativeEligibilityFactory(household_structure=household_structure)
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
        dob1 = date.today() - relativedelta(years=hm1.age_in_years)
        dob2 = date.today() - relativedelta(years=hm2.age_in_years)
        dob3 = date.today() - relativedelta(years=hm3.age_in_years)
        ec1 = EnrollmentChecklistFactory(
            household_member=hm1,
            initials=hm1.initials,
            gender=hm1.gender,
            dob=dob1)
        ec2 = EnrollmentChecklistFactory(
            household_member=hm2,
            initials=hm2.initials,
            gender=hm2.gender,
            dob=dob2)
        ec3 = EnrollmentChecklistFactory(
            household_member=hm3,
            initials=hm3.initials,
            gender=hm3.gender,
            dob=dob3)
        print 'hm1', hm1.member_status
        print 'hm2', hm2.member_status
        print 'hm3', hm3.member_status
        SubjectConsentFactory(first_name='THING1',
                              survey=survey1,
                              household_member=hm1,
                              registered_subject=hm1.registered_subject,
                              dob=dob1,
                              initials=hm1.initials,
                              study_site=self.study_site)
        SubjectConsentFactory(first_name='THING2',
                              survey=survey1,
                              household_member=hm2,
                              registered_subject=hm2.registered_subject,
                              dob=dob2,
                              initials=hm2.initials,
                              study_site=self.study_site)
        subject_consent = SubjectConsentFactory(
            first_name='THING3',
            survey=survey1,
            household_member=hm3,
            registered_subject=hm3.registered_subject,
            dob=dob3,
            initials=hm3.initials,
            study_site=self.study_site)
        print 'Subject consent updates registered_subject'
        self.assertEqual(dob1, hm1.registered_subject.dob, 'Expected enrollment checklist dob {0} for registered_subject. Got {1}'.format(dob1, hm1.registered_subject.dob))
        self.assertEqual(dob2, hm2.registered_subject.dob, 'Expected enrollment checklist dob {0} for registered_subject. Got {1}'.format(dob2, hm2.registered_subject.dob))
        self.assertEqual(dob3, hm3.registered_subject.dob, 'Expected enrollment checklist dob {0} for registered_subject. Got {1}'.format(dob3, hm3.registered_subject.dob))

        print 'assert has consent history methods'
        self.assertTrue('get_consent_history_model' in dir(subject_consent))
        self.assertTrue('update_consent_history' in dir(subject_consent))
        self.assertTrue('delete_consent_history' in dir(subject_consent))
        print 'confirm RS created'
        self.assertEquals(RegisteredSubject.objects.all().count(), 3)
        self.assertEquals(RegisteredSubject.objects.filter(first_name=subject_consent.first_name, dob=subject_consent.dob, initials=subject_consent.initials).count(), 1)
        print 'assert get_consent_history_model returns a model of base class BaseConsentHistory'
        history_model = subject_consent.get_consent_history_model()
        self.assertIsNotNone(subject_consent.get_consent_history_model())
        print 'assert consent history now includes consent for {0}'.format(subject_consent)
        self.assertEquals(history_model.objects.filter(registered_subject=subject_consent.registered_subject).count(), 1)
        subject_consent_history = history_model.objects.get(registered_subject=subject_consent.registered_subject, consent_pk=subject_consent.pk)
        self.assertEqual(subject_consent.consent_datetime, subject_consent_history.consent_datetime)
        print 'update consent for {0}'.format(subject_consent)
        subject_consent.consent_datetime = datetime.today()
        subject_consent.save()
        print 'assert history updated for {0}'.format(subject_consent)
        subject_consent_history = history_model.objects.get(registered_subject=subject_consent.registered_subject, consent_pk=subject_consent.pk)
        self.assertEqual(subject_consent.consent_datetime, subject_consent_history.consent_datetime)
        print 'delete consent for {0}'.format(subject_consent)
        subject_consent.delete()
        print 'assert history update for {0}'.format(subject_consent)
        self.assertEqual(history_model.objects.filter(registered_subject=subject_consent.registered_subject, consent_pk=subject_consent.pk).count(), 0)
        self.assertEqual(history_model.objects.all().count(), 3)
