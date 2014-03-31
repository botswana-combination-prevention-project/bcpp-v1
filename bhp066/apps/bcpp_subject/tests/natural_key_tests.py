from datetime import datetime, timedelta, date

from django.core import serializers
from django.db.models import get_app, get_models
from django.test import TestCase

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.map.classes import Mapper, site_mappers
from edc.subject.lab_tracker.classes import site_lab_tracker

from edc.core.bhp_variables.models import StudySite
from edc.core.crypto_fields.classes import FieldCryptor
from edc.device.sync.classes import SerializeToTransaction
from edc.subject.registration.models import RegisteredSubject
from edc.subject.visit_schedule.models import VisitDefinition
from edc.entry_meta_data.models import ScheduledEntryMetaData
from edc.subject.entry.models import Entry
from edc.subject.appointment.models import Appointment

from apps.bcpp.app_configuration.classes import BcppAppConfiguration
from apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule
from apps.bcpp_household.models import Household, HouseholdStructure
from apps.bcpp_household.tests.factories import PlotFactory
from apps.bcpp_household_member.tests.factories import HouseholdMemberFactory, EnrollmentChecklistFactory
from apps.bcpp_subject.tests.factories import SubjectConsentFactory
from apps.bcpp_subject.tests.factories import (SubjectVisitFactory, SubjectLocatorFactory,
                                               SubjectDeathFactory, SubjectReferralFactory)
from apps.bcpp_survey.models import Survey


class NaturalKeyTests(TestCase):

    def setUp(self):
        try:
            site_lab_profiles.register(BcppSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        BcppAppConfiguration()
        site_lab_tracker.autodiscover()
        BcppSubjectVisitSchedule().build()

    def test_p1(self):
        """Confirms all models have a natural_key method (except Audit models)"""
        app = get_app('bcpp_subject')
        for model in get_models(app):
            if 'Audit' not in model._meta.object_name:
                print 'checking for natural key on {0}.'.format(model._meta.object_name)
                self.assertTrue('natural_key' in dir(model), 'natural key not found in {0}'.format(model._meta.object_name))

    def test_p2(self):
        """Confirms all models have a get_by_natural_key manager method."""
        app = get_app('bcpp_subject')
        for model in get_models(app):
            if 'Audit' not in model._meta.object_name:
                print 'checking for get_by_natural_key manager method key on {0}.'.format(model._meta.object_name)
                self.assertTrue('get_by_natural_key' in dir(model.objects), 'get_by_natural_key key not found in {0}'.format(model._meta.object_name))

    def test_p3(self):
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

        household_member = HouseholdMemberFactory(household_structure=household_structure)
        enrollment_checklist = EnrollmentChecklistFactory(household_member=household_member, initials=household_member.initials, has_identity='Yes', dob=date(1989,01,01))
        study_site = StudySite.objects.all()[0]
        subject_consent = SubjectConsentFactory(study_site=study_site, household_member=household_member, registered_subject=household_member.registered_subject,
                                                dob=enrollment_checklist.dob, initials=enrollment_checklist.initials)
        print subject_consent.subject_identifier
        print 'get registered subject'
        registered_subject = RegisteredSubject.objects.get(subject_identifier=subject_consent.subject_identifier)
        instances = []
        instances.append(subject_consent)
        instances.append(registered_subject)

        print 'test natural key / get_by_natural_key on subject_visit'
        print 'No. of ENTRIES = '+str(Entry.objects.all().count())
#         content_type = ContentType.objects.get(app_label='bcpp_subject', model='subjectvisit')
#         content_type_map = ContentTypeMap.objects.get(content_type=content_type)
        self.assertEqual(VisitDefinition.objects.all().count(), 1)
        visit_definition = VisitDefinition.objects.get(title = 'T0') #VisitDefinitionFactory(visit_tracking_content_type_map=content_type_map)
        print 'No. of Appointments = '+str(Appointment.objects.all().count())
        appointment = Appointment.objects.get(visit_definition=visit_definition)
        print 'No. of ScheduledEntryMetaData before Visit = '+str(ScheduledEntryMetaData.objects.all().count())
        subject_visit = SubjectVisitFactory(appointment=appointment, household_member=household_member)
        print 'No. of ScheduledEntryMetaData after Visit = '+str(ScheduledEntryMetaData.objects.all().count())
        subject_referral = SubjectReferralFactory(subject_visit=subject_visit)
        # SubjectDeath : Independent Natural Keys
        subject_death = SubjectDeathFactory(registered_subject=registered_subject)
        # SubjectLocator : Independent Natural Key
        subject_locator = SubjectLocatorFactory(subject_visit=subject_visit, registered_subject=registered_subject)
        instances.append(subject_referral)
        instances.append(subject_death)
        instances.append(subject_locator)

        print 'INSTANCE: ' + str(instances)
        for obj in instances:
            print 'test natural key on {0}'.format(obj._meta.object_name)
            natural_key = obj.natural_key()
            get_obj = obj.__class__.objects.get_by_natural_key(*natural_key)
            self.assertEqual(obj.pk, get_obj.pk)
        # pp = pprint.PrettyPrinter(indent=4)
        for obj in instances:
            print 'test serializing/deserializing {0}'.format(obj._meta.object_name)
            outgoing_transaction = SerializeToTransaction().serialize(obj.__class__, obj)
            # pp.pprint(FieldCryptor('aes', 'local').decrypt(outgoing_transaction.tx))
            for transaction in serializers.deserialize("json", FieldCryptor('aes', 'local').decrypt(outgoing_transaction.tx)):
                self.assertEqual(transaction.object.pk, obj.pk)
