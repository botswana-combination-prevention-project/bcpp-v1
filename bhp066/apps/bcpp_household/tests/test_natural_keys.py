from datetime import datetime, date, timedelta
from django.test import TestCase, SimpleTestCase
from django.core import serializers
from edc_base.encrypted_fields import FieldCryptor
from django.db.models import get_app, get_models

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.device.sync.classes import SerializeToTransaction
from edc.map.classes import site_mappers

from bhp066.apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from bhp066.apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule
from bhp066.apps.bcpp_survey.models import Survey

from ..models import Household, HouseholdStructure, HouseholdLog, HouseholdRefusal
from .factories import (PlotFactory, PlotLogEntryFactory, HouseholdLogEntryFactory, HouseholdRefusalFactory,
                        PlotLogFactory, HouseholdAssessmentFactory)


class TestNaturalKeys(SimpleTestCase):

    def startup(self):
        from bhp066.apps.bcpp.app_configuration.classes import BcppAppConfiguration
        try:
            site_lab_profiles.register(BcppSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        BcppAppConfiguration()
        site_lab_tracker.autodiscover()
        BcppSubjectVisitSchedule().build()

    def test_p1(self):
        """Confirms all models have a natural_key method (except Audit models)"""
        self.startup()
        app = get_app('bcpp_household')
        for model in get_models(app):
            if 'Audit' not in model._meta.object_name:
                print 'checking for natural key on {0}.'.format(model._meta.object_name)
                self.assertTrue('natural_key' in dir(model), 'natural key not found in {0}'.format(model._meta.object_name))

    def test_p2(self):
        """Confirms all models have a get_by_natural_key manager method."""
        self.startup()
        survey = Survey.objects.all()[0]
        print 'get a community name from the mapper classes'
        community = site_mappers.get_as_list()[0]
        site_mappers.autodiscover()
        mapper = site_mappers.get(site_mappers.get_as_list()[0])
        print 'No. of SURVEY = ' + str(Survey.objects.all().count())
        plot = PlotFactory(community=mapper().get_map_area(), status='residential_habitable')
        plot.save()
        print 'No. of HOUSEHOLDS = ' + str(Household.objects.all().count())
        household = Household.objects.get(plot=plot)
        self.assertEquals(HouseholdStructure.objects.all().count(), 3)
        self.assertEquals(Survey.objects.all().count(), 3)
        household_structure = HouseholdStructure.objects.get(survey=Survey.objects.all()[0])
        print 'No. of HOUSEHOLDS_STRUCTURE = ' + str(HouseholdStructure.objects.all().count())
        household_refusal = HouseholdRefusalFactory(household_structure=household_structure)
        print 'No. of HOUSEHOLDS_REFUSALS = ' + str(HouseholdRefusal.objects.all().count())
        print 'HOUSEHOLD_REFUSAL=' + str(HouseholdRefusal.objects.all()[0]) 
#         household_identifier_history =
        HouseholdRefusal.objects.get(household_structure=household_structure).delete()
        print 'No. of HOUSEHOLDS_REFUSALS = ' + str(HouseholdRefusal.objects.all().count())
#         self.assertEqual(HouseholdRefusalHistory.objects.all().count(), 1)
#         household_ref_history = HouseholdRefusalHistory.objects.get(household_structure=household_structure)
        household_structure.failed_enumeration_attempts = 3
        household_assesment = HouseholdAssessmentFactory(household_structure=household_structure)
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
        #instances.append(household_refusal)
        instances.append(household_assesment)
#         instances.append(household_ref_history)
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
            outgoing_transaction = SerializeToTransaction().serialize(obj.__class__, obj, False, True, 'default')
            # pp.pprint(FieldCryptor('aes', 'local').decrypt(outgoing_transaction.tx))
            for transaction in serializers.deserialize("json", FieldCryptor('aes', 'local').decrypt(outgoing_transaction.tx)):
                self.assertEqual(transaction.object.pk, obj.pk)
