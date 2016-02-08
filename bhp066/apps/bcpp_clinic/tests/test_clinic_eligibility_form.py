from django.core import serializers
from django.db.models import get_app, get_models
from django.test import TestCase
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.test.utils import override_settings

from edc.lab.lab_profile.classes import site_lab_profiles
from edc_base.encrypted_fields import FieldCryptor
from edc.device.sync.classes import SerializeToTransaction
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.appointment.models import Appointment
from edc.subject.registration.models import RegisteredSubject
from edc.map.classes import Mapper, site_mappers
from edc_constants.constants import YES, NO, MALE

from bhp066.apps.bcpp_clinic.tests.factories import ClinicEligibilityFactory, ClinicEnrollmentLossFactory
from bhp066.apps.bcpp_clinic.tests.factories import (ClinicConsentFactory, ClinicVisitFactory,
                                             ClinicLocatorFactory, QuestionnaireFactory)
from edc.subject.registration.tests.factories import RegisteredSubjectFactory
from bhp066.apps.bcpp_clinic.models import ClinicEnrollmentLoss
from bhp066.apps.bcpp.app_configuration.classes import BcppAppConfiguration
from bhp066.apps.bcpp_clinic.visit_schedule import BcppClinicVisitSchedule
from bhp066.apps.bcpp_household.tests.factories.household_structure_factory import HouseholdStructureFactory
from bhp066.apps.bcpp_household.tests.factories.plot_factory import PlotFactory
from bhp066.apps.bcpp_household_member.tests.factories import HouseholdMemberFactory
from bhp066.apps.bcpp_household.tests.factories import HouseholdFactory
from bhp066.apps.bcpp_lab.lab_profiles import ClinicSubjectProfile


class TestNaturalKey(TestCase):

    community = 'digawana'

    def setUp(self):
        try:
            site_lab_profiles.register(ClinicSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        site_mappers.autodiscover()
        BcppAppConfiguration().prepare()
        site_lab_tracker.autodiscover()
        BcppClinicVisitSchedule().build()
        plot = PlotFactory(community=self.communitys)
        household = HouseholdFactory(plot=plot)
        household_structure = HouseholdStructureFactory(household=household)
        household_member = HouseholdMemberFactory(household_structure=household_structure)
        self.data = {
            'household_member': household_member.id,
            'report_datetime': datetime.today(),
            'first_name': 'Sets',
            'initials': 'SA',
            'dob': datetime.today() + relativedelta(years=-20),
            'guardian': NO,
            'gender': MALE,
            'has_identity': YES,
            'identity': '317918515',
            'identity_type': 'omang',
            'citizen': YES,

        }

    def test_no_identity_validation(self):
        from bhp066.apps.bcpp_clinic.forms.clinic_eligibility_form import ClinicEligibilityForm
        clinic_form = ClinicEligibilityForm(data=self.data)
        print clinc_form.errors

    def test_with_identity_validation(self):
        pass

    def test_with_identity_validation(self):
        pass

