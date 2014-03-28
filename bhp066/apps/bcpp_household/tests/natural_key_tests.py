from datetime import datetime, date, timedelta
from django.test import TestCase
from django.core import serializers
from edc.core.crypto_fields.classes import FieldCryptor
from django.db.models import get_app, get_models

from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.device.sync.classes import SerializeToTransaction
from edc.map.classes import site_mappers
from edc.core.bhp_variables.tests.factories import StudySpecificFactory, StudySiteFactory
from edc.subject.consent.tests.factories import ConsentCatalogueFactory
from edc.core.bhp_content_type_map.classes import ContentTypeMapHelper
from edc.core.bhp_content_type_map.models import ContentTypeMap
from apps.bcpp_survey.models import Survey

from apps.bcpp_household.models import Household, HouseholdStructure, HouseholdLog, HouseholdRefusal
from apps.bcpp_household.tests.factories import (PlotFactory, PlotLogEntryFactory, HouseholdLogEntryFactory, HouseholdRefusalFactory,
                                                 PlotLogFactory, HouseholdLogFactory)


class NaturalKeyTests(TestCase):

    def test_p1(self):
        """Confirms all models have a natural_key method (except Audit models)"""
        app = get_app('bcpp_household')
        for model in get_models(app):
            if 'Audit' not in model._meta.object_name:
                print 'checking for natural key on {0}.'.format(model._meta.object_name)
                self.assertTrue('natural_key' in dir(model), 'natural key not found in {0}'.format(model._meta.object_name))

    def test_p2(self):
        """Confirms all models have a get_by_natural_key manager method."""
        app = get_app('bcpp_household')
        for model in get_models(app):
            if 'Audit' not in model._meta.object_name:
                print 'checking for get_by_natural_key manager method key on {0}.'.format(model._meta.object_name)
                self.assertTrue('get_by_natural_key' in dir(model.objects), 'get_by_natural_key key not found in {0}'.format(model._meta.object_name))

        site_lab_tracker.autodiscover()
        StudySpecificFactory()
        StudySiteFactory()
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
        print 'get a community name from the mapper classes'
        community = site_mappers.get_as_list()[0]
        site_mappers.autodiscover()
        mapper = site_mappers.get(site_mappers.get_as_list()[0])
        print 'No. of SURVEY = ' + str(Survey.objects.all().count())
        plot = PlotFactory(community=mapper().get_map_area())
        print 'No. of HOUSEHOLDS = ' + str(Household.objects.all().count())
        household = Household.objects.get(plot=plot)
        self.assertEquals(HouseholdStructure.objects.all().count(), 1)
        self.assertEquals(Survey.objects.all().count(), 1)
        household_structure = HouseholdStructure.objects.get(survey=Survey.objects.all()[0])
        household_refusal = HouseholdRefusalFactory(household=household)
        print 'No. of HOUSEHOLDS_REFUSALS = ' + str(HouseholdRefusal.objects.all().count())
#         household_identifier_history =
        print 'No. of HOUSEHOLDS_STRUCTURE = ' + str(HouseholdStructure.objects.all().count())
        print 'No. of HOUSEHOLDS_LOG = ' + str(HouseholdLog.objects.all().count())
        household_log = HouseholdLog.objects.get(household_structure=household_structure)
        household_log_entry1 = HouseholdLogEntryFactory(household_log=household_log, report_datetime=date.today())
        household_log_entry2 = HouseholdLogEntryFactory(household_log=household_log, report_datetime=date.today() + timedelta(days=1))
#         plot_identifier_history =
        plot_log = PlotLogFactory(plot=plot)
        plot_log_entry1 = PlotLogEntryFactory(plot_log=plot_log, report_datetime=datetime.now())
        plot_log_entry2 = PlotLogEntryFactory(plot_log=plot_log, report_datetime=datetime.now() + timedelta(days=1))

        instances = []
        instances.append(plot)
        instances.append(household)
        # instances.append(enrollment_checklist)
        instances.append(household_structure)
        instances.append(household_refusal)
#         instances.append(household_identifier_history)
        instances.append(household_log)
        instances.append(plot_log_entry1)
        instances.append(plot_log_entry2)
#         instances.append(plot_identifier_history)

        instances.append(plot_log)
        instances.append(household_log_entry1)
        instances.append(household_log_entry2)

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
