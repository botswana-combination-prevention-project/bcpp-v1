from datetime import datetime, date, timedelta
from django.test import SimpleTestCase
from django.core import serializers
from edc_base.encrypted_fields import FieldCryptor
from django.db.models import get_app, get_models

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.device.sync.classes import SerializeToTransaction


from edc.subject.rule_groups.classes import site_rule_groups

from bhp066.apps.bcpp.app_configuration.classes import BcppAppConfiguration
from bhp066.apps.bcpp_household.models import Household, HouseholdStructure, HouseholdLog, HouseholdRefusal
from bhp066.apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from bhp066.apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule
from bhp066.apps.bcpp_survey.models import Survey

from .factories.plot_factory import PlotFactory
from .factories.plot_log_factory import PlotLogFactory
from .factories.plot_log_entry_factory import PlotLogEntryFactory
from .factories.household_log_entry_factory import HouseholdLogEntryFactory
from .factories.household_refusal_factory import HouseholdRefusalFactory
from .factories.household_assessment_factory import HouseholdAssessmentFactory


class TestNaturalKeys(SimpleTestCase):

    def setUp(self):
        try:
            site_lab_profiles.register(BcppSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        BcppAppConfiguration().prepare()
        site_lab_tracker.autodiscover()
        BcppSubjectVisitSchedule().build()
        site_rule_groups.autodiscover()
        self.community = 'test_community'

    def test_p1(self):
        """Confirms all models have a natural_key method (except Audit models)"""
        app = get_app('bcpp_household')
        for model in get_models(app):
            if 'Audit' not in model._meta.object_name:
                self.assertTrue('natural_key' in dir(model), 'natural key not found in {0}'.format(model._meta.object_name))

    def test_p2(self):
        """Confirms all models have a get_by_natural_key manager method."""
        plot = PlotFactory(community=self.community, status='residential_habitable')
        plot.save()
        household = Household.objects.get(plot=plot)
        self.assertEquals(HouseholdStructure.objects.all().count(), 3)
        self.assertEquals(Survey.objects.all().count(), 3)
        household_structure = HouseholdStructure.objects.get(survey=Survey.objects.all()[0])
        HouseholdRefusalFactory(household_structure=household_structure)
        HouseholdRefusal.objects.get(household_structure=household_structure).delete()
        household_structure.failed_enumeration_attempts = 3
        household_assesment = HouseholdAssessmentFactory(household_structure=household_structure)
        household_log = HouseholdLog.objects.get(household_structure=household_structure)
        household_log_entry1 = HouseholdLogEntryFactory(household_log=household_log, report_datetime=date.today())
        household_log_entry2 = HouseholdLogEntryFactory(household_log=household_log, report_datetime=date.today() + timedelta(days=1))
        plot_log = PlotLogFactory(plot=plot)
        plot_log_entry1 = PlotLogEntryFactory(plot_log=plot_log, report_datetime=datetime.now())
        plot_log_entry2 = PlotLogEntryFactory(plot_log=plot_log, report_datetime=datetime.now() + timedelta(days=1))

        instances = []
        instances.append(plot)
        instances.append(household)
        instances.append(household_structure)
        instances.append(household_assesment)
        instances.append(household_log)
        instances.append(plot_log_entry1)
        instances.append(plot_log_entry2)

        instances.append(plot_log)
        instances.append(household_log_entry1)
        instances.append(household_log_entry2)

        for obj in instances:
            natural_key = obj.natural_key()
            get_obj = obj.__class__.objects.get_by_natural_key(*natural_key)
            self.assertEqual(obj.pk, get_obj.pk)
        for obj in instances:
            outgoing_transaction = SerializeToTransaction().serialize(obj.__class__, obj, False, True, 'default')
            for transaction in serializers.deserialize("json", FieldCryptor('aes', 'local').decrypt(outgoing_transaction.tx)):
                self.assertEqual(transaction.object.pk, obj.pk)
