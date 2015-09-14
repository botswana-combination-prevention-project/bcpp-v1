from datetime import datetime, date
from django.test import TestCase
from dateutil.relativedelta import relativedelta
from edc.constants import NEW, NOT_REQUIRED, KEYED, REQUIRED, POS, NEG
from edc.entry_meta_data.models import ScheduledEntryMetaData, RequisitionMetaData
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.map.classes import Mapper, site_mappers
from edc.subject.appointment.models import Appointment
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.registration.models import RegisteredSubject
from edc.subject.rule_groups.classes import site_rule_groups
from edc.core.bhp_variables.models import StudySite

from apps.bcpp_household.models import HouseholdStructure
from apps.bcpp_household.tests.factories import PlotFactory, RepresentativeEligibilityFactory
from apps.bcpp_household_member.tests.factories import HouseholdMemberFactory, EnrollmentChecklistFactory
from apps.bcpp_household_member.classes  import EnumerationHelper
from apps.bcpp_survey.models import Survey

from apps.bcpp.app_configuration.classes import BcppAppConfiguration
from apps.bcpp_lab.tests.factories import SubjectRequisitionFactory
from apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from apps.bcpp_lab.models import AliquotType, Panel
from apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule
from apps.bcpp_subject.models import HivResult

from .factories import (SubjectConsentFactory, SubjectVisitFactory)


class BaseRuleGroupTestSetup(TestCase):
    app_label = 'bcpp_subject'
    community = 'otse'

    def setUp(self):
        try:
            site_lab_profiles.register(BcppSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        BcppAppConfiguration().prepare()
        site_lab_tracker.autodiscover()
        BcppSubjectVisitSchedule().build()
        site_rule_groups.autodiscover()

        plot = PlotFactory(community=self.community, household_count=1, status='residential_habitable')

        survey = Survey.objects.all().order_by('datetime_start')[0]
        next_survey = Survey.objects.all().order_by('datetime_start')[1]

        self.study_site = StudySite.objects.get(site_code='14')

        self.household_structure = HouseholdStructure.objects.get(household__plot=plot, survey=survey)
        self.household_structure_y2 = HouseholdStructure.objects.get(household__plot=plot, survey=next_survey)
        RepresentativeEligibilityFactory(household_structure=self.household_structure)
        RepresentativeEligibilityFactory(household_structure=self.household_structure_y2)
        HouseholdMemberFactory(household_structure=self.household_structure)
        HouseholdMemberFactory(household_structure=self.household_structure)
        HouseholdMemberFactory(household_structure=self.household_structure)

        male_dob = date.today() - relativedelta(years=25)
        male_age_in_years = 25
        male_first_name = 'ERIK'
        male_initials = "EW"
        female_dob = date.today() - relativedelta(years=35)
        female_age_in_years = 35
        female_first_name = 'ERIKA'
        female_initials = "EW"

        self.household_member_female_T0 = HouseholdMemberFactory(household_structure=self.household_structure, gender='F', age_in_years=female_age_in_years, first_name=female_first_name, initials=female_initials)
        self.household_member_male_T0 = HouseholdMemberFactory(household_structure=self.household_structure, gender='M', age_in_years=male_age_in_years, first_name=male_first_name, initials=male_initials)
        self.household_member_female_T0.member_status = 'BHS_SCREEN'
        self.household_member_male_T0.member_status = 'BHS_SCREEN'
        self.household_member_female_T0.save()
        self.household_member_male_T0.save()
        EnrollmentChecklistFactory(
            household_member=self.household_member_female_T0,
            gender='F',
            citizen='Yes',
            dob=female_dob,
            guardian='No',
            initials=self.household_member_female_T0.initials,
            part_time_resident='Yes')
        EnrollmentChecklistFactory(
            household_member=self.household_member_male_T0,
            gender='M',
            citizen='Yes',
            dob=male_dob,
            guardian='No',
            initials=self.household_member_male_T0.initials,
            part_time_resident='Yes')
        subject_consent_female = SubjectConsentFactory(household_member=self.household_member_female_T0, study_site=self.study_site, gender='F', dob=female_dob, first_name=female_first_name, initials=female_initials)
        subject_consent_male = SubjectConsentFactory(household_member=self.household_member_male_T0, study_site=self.study_site, gender='M', dob=male_dob, first_name=male_first_name, initials=male_initials)

        enumeration_helper = EnumerationHelper(self.household_structure.household, survey, next_survey)
        self.household_member_female = enumeration_helper.create_member_on_target(self.household_member_female_T0)
        self.household_member_male = enumeration_helper.create_member_on_target(self.household_member_male_T0)

        self.registered_subject_female = RegisteredSubject.objects.get(subject_identifier=subject_consent_female.subject_identifier)
        self.registered_subject_male = RegisteredSubject.objects.get(subject_identifier=subject_consent_male.subject_identifier)
        self.appointment_female = Appointment.objects.get(registered_subject=self.registered_subject_female, visit_definition__code='T1')
        self.appointment_female_T0 = Appointment.objects.get(registered_subject=self.registered_subject_female, visit_definition__code='T0')
        self.subject_visit_female_T0 = SubjectVisitFactory(appointment=self.appointment_female_T0, household_member=self.household_member_female_T0)
        self.subject_visit_female = SubjectVisitFactory(appointment=self.appointment_female, household_member=self.household_member_female)
        self.appointment_male = Appointment.objects.get(registered_subject=self.registered_subject_male, visit_definition__code='T1')
        self.appointment_male_T0 = Appointment.objects.get(registered_subject=self.registered_subject_male, visit_definition__code='T0')
        self.subject_visit_male_T0 = SubjectVisitFactory(appointment=self.appointment_male_T0, household_member=self.household_member_male_T0)
        self.subject_visit_male = SubjectVisitFactory(appointment=self.appointment_male, household_member=self.household_member_male)

    def check_male_registered_subject_rule_groups(self, subject_visit):
        circumsition_options = {}
        circumsition_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='circumcision',
            appointment=subject_visit.appointment)

        circumcised_options = {}
        circumcised_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='circumcised',
            appointment=subject_visit.appointment)

        uncircumcised_options = {}
        uncircumcised_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='uncircumcised',
            appointment=subject_visit.appointment)

        reproductivehealth_options = {}
        reproductivehealth_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='reproductivehealth',
            appointment=subject_visit.appointment)

        pregnancy_options = {}
        pregnancy_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pregnancy',
            appointment=subject_visit.appointment)

        nonpregnancy_options = {}
        nonpregnancy_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='nonpregnancy',
            appointment=subject_visit.appointment)

        if subject_visit == self.subject_visit_male_T0:
            self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **circumsition_options).count(), 1)
            self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **circumcised_options).count(), 1)
            self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **uncircumcised_options).count(), 1)
            self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **reproductivehealth_options).count(), 1)
            self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **pregnancy_options).count(), 1)
            self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **nonpregnancy_options).count(), 1)
        else:
            self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **reproductivehealth_options).count(), 1)
            self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **pregnancy_options).count(), 1)
            self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **nonpregnancy_options).count(), 1)
            self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **circumsition_options).count(), 1)
            self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **circumcised_options).count(), 1)
            self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **uncircumcised_options).count(), 1)

    def new_metadata_is_not_keyed(self):
        self.assertEquals(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, appointment=self.subject_visit_male.appointment).count(), 0)
        self.assertEquals(RequisitionMetaData.objects.filter(entry_status=KEYED, appointment=self.subject_visit_male.appointment).count(), 0)

    @property
    def baseline_subject_visit(self):
        """ Return baseline subject visit"""
        self.subject_visit_male_T0.delete()
        self.subject_visit_male_T0 = SubjectVisitFactory(appointment=self.appointment_male_T0, household_member=self.household_member_male_T0)
        self.check_male_registered_subject_rule_groups(self.subject_visit_male_T0)
        return self.subject_visit_male_T0

    @property
    def annual_subject_visit(self):
        """ Return annuall subject visit """
        self.subject_visit_male.delete()
        self.assertEqual(ScheduledEntryMetaData.objects.filter(appointment=self.appointment_male).count(), 0)
        self.subject_visit_male = SubjectVisitFactory(appointment=self.appointment_male, household_member=self.household_member_male)
        #self.check_male_registered_subject_rule_groups(self.subject_visit_male)
        return self.subject_visit_male

    def hiv_result(self, status, subject_visit):
        """ Create HivResult for a particular survey"""
        aliquot_type = AliquotType.objects.all()[0]
        site = StudySite.objects.all()[0]
        microtube_panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=subject_visit, panel=microtube_panel, aliquot_type=aliquot_type, site=site)

        self._hiv_result = HivResult.objects.create(
             subject_visit=subject_visit,
             hiv_result=status,
             report_datetime=datetime.today(),
             insufficient_vol='No'
            )
        return self._hiv_result