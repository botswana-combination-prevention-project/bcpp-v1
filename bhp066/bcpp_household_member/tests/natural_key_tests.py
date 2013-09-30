from datetime import datetime, timedelta
from django.test import TestCase
from django.db.models import signals
from django.core import serializers
from django.db.models import get_app, get_models
from edc.core.bhp_crypto.classes import FieldCryptor
from edc.core.bhp_lab_tracker.classes import site_lab_tracker
from edc.core.bhp_sync.classes import SerializeToTransaction
from edc.core.bhp_variables.tests.factories import StudySpecificFactory, StudySiteFactory
from edc.core.bhp_registration.models import RegisteredSubject
from edc.core.bhp_consent.tests.factories import ConsentCatalogueFactory
from edc.core.bhp_appointment.tests.factories import ConfigurationFactory
from edc.core.bhp_content_type_map.classes import ContentTypeMapHelper
from edc.core.bhp_content_type_map.models import ContentTypeMap
from bcpp_survey.models import Survey
from bcpp_household.tests.factories import HouseholdStructureFactory
from bcpp_household.models import create_household_structure_on_post_save
from .factories import HouseholdMemberFactory, EnrolmentChecklistFactory, HouseholdInfoFactory


class NaturalKeyTests(TestCase):

    def test_p1(self):
        """Confirms all models have a natural_key method (except Audit models)"""
        app = get_app('bcpp_household_member')
        for model in get_models(app):
            if 'Audit' not in model._meta.object_name:
                print 'checking for natural key on {0}.'.format(model._meta.object_name)
                self.assertTrue('natural_key' in dir(model), 'natural key not found in {0}'.format(model._meta.object_name))

    def test_p2(self):
        """Confirms all models have a get_by_natural_key manager method."""
        app = get_app('bcpp_household_member')
        for model in get_models(app):
            if 'Audit' not in model._meta.object_name:
                print 'checking for get_by_natural_key manager method key on {0}.'.format(model._meta.object_name)
                self.assertTrue('get_by_natural_key' in dir(model.objects), 'get_by_natural_key key not found in {0}'.format(model._meta.object_name))

    def test_p3(self):
        site_lab_tracker.autodiscover()
        StudySpecificFactory()
        StudySiteFactory()
        ConfigurationFactory()
        content_type_map_helper = ContentTypeMapHelper()
        content_type_map_helper.populate()
        content_type_map_helper.sync()
        print 'setup the consent catalogue for this BCPP'
        content_type_map = ContentTypeMap.objects.get(content_type__model__iexact='SubjectConsent')
        print ContentTypeMap.objects.all().count()
        consent_catalogue = ConsentCatalogueFactory(name='bcpp year 0', content_type_map=content_type_map)
        consent_catalogue.add_for_app = 'bcpp_subject'
        consent_catalogue.save()
        Survey.objects.create(survey_name='YEAR 0',
                          datetime_start=datetime.today() - timedelta(days=30),
                          datetime_end=datetime.today() + timedelta(days=180)
                          )
        survey = Survey.objects.all()[0]
#         print 'Clear previous Registered Subjects: Count='+str(RegisteredSubject.objects.all().count())
#         RegisteredSubject.objects.all().delete()
        signals.post_save.disconnect(create_household_structure_on_post_save, weak=False, dispatch_uid="create_household_structure_on_post_save")
        household_structure = HouseholdStructureFactory(survey=survey)
        signals.post_save.connect(create_household_structure_on_post_save, weak=False, dispatch_uid="create_household_structure_on_post_save")
        household_member = HouseholdMemberFactory(household_structure=household_structure, survey=survey)
        print 'get registered subject'
        registered_subject = RegisteredSubject.objects.get(subject_identifier=household_member.registered_subject.subject_identifier)
        enrolment_checklist = EnrolmentChecklistFactory(household_member=household_member, registered_subject=registered_subject)
        household_info = HouseholdInfoFactory()
        # contact_log = ContactLogFactory()
        # contact_log_item = ContactLogFactoryItem()
        instances = []
        instances.append(household_member)
        instances.append(registered_subject)
        instances.append(enrolment_checklist)
        instances.append(household_structure)
        instances.append(household_info)
        # instances.append(contact_log)
        # instances.append(contact_log_item)

        print 'test natural key / get_by_natural_key on subject_visit'

#         appointment, created = Appointment.objects.get_or_create(registered_subject=registered_subject,
#                                                                  appt_datetime = datetime.today(),
#                                                                  visit_definition__code='1000')
#         content_type = ContentType.objects.get(app_label='bcpp_subject',model='subjectvisit')
#         content_type_map = ContentTypeMap.objects.get(content_type=content_type)

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
