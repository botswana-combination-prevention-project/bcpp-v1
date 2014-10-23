from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

from django.test import TestCase

from edc.constants import NEW, NOT_REQUIRED, KEYED, REQUIRED
from edc.entry_meta_data.models import ScheduledEntryMetaData, RequisitionMetaData
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.map.classes import Mapper, site_mappers
from edc.subject.appointment.models import Appointment
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.registration.models import RegisteredSubject
from edc.subject.rule_groups.classes import site_rule_groups
from edc.subject.visit_schedule.classes import site_visit_schedules
from edc.core.bhp_variables.models import StudySite

from apps.bcpp_household.models import HouseholdStructure
from apps.bcpp_household.tests.factories import PlotFactory, RepresentativeEligibilityFactory
from apps.bcpp_subject.tests.factories import HivTestingHistoryFactory
from apps.bcpp_household_member.tests.factories import HouseholdMemberFactory, EnrollmentChecklistFactory
from apps.bcpp_survey.models import Survey
from apps.bcpp_survey.tests.factories import SurveyFactory
from apps.bcpp_lab.tests.factories import SubjectRequisitionFactory
from apps.bcpp_lab.models import Panel, AliquotType
from apps.bcpp_list.models import Diagnoses

from apps.bcpp.app_configuration.classes import BcppAppConfiguration
from apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule

from ..models import HivCareAdherence, HivTestingHistory, HivTestReview, HivResult, ElisaHivResult
from .factories import SubjectConsentFactory, SubjectVisitFactory, HivCareAdherenceFactory, MedicalDiagnosesFactory


class TestPlotMapper(Mapper):
    map_area = 'test_community9'
    map_code = '097'
    regions = []
    sections = []
    landmarks = []
    gps_center_lat = -25.033162
    gps_center_lon = 25.747149
    radius = 5.5
    location_boundary = ()

site_mappers.register(TestPlotMapper)


class TestRuleGroup(TestCase):

    app_label = 'bcpp_subject'
    community = 'test_community9'

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

        study_site = StudySite.objects.get(site_code='16')

        household_structure = HouseholdStructure.objects.get(household__plot=plot, survey=survey)
        RepresentativeEligibilityFactory(household_structure=household_structure)
        HouseholdMemberFactory(household_structure=household_structure)
        HouseholdMemberFactory(household_structure=household_structure)
        HouseholdMemberFactory(household_structure=household_structure)

        male_dob = date.today() - relativedelta(years=25)
        male_age_in_years = 25
        male_first_name = 'ERIK'
        male_initials = "EW"
        female_dob = date.today() - relativedelta(years=35)
        female_age_in_years = 35
        female_first_name = 'ERIKA'
        female_initials = "EW"

        self.household_member_female = HouseholdMemberFactory(household_structure=household_structure, gender='F', age_in_years=female_age_in_years, first_name=female_first_name, initials=female_initials)
        self.household_member_male = HouseholdMemberFactory(household_structure=household_structure, gender='M', age_in_years=male_age_in_years, first_name=male_first_name, initials=male_initials)
        self.household_member_female.member_status = 'BHS_SCREEN'
        self.household_member_male.member_status = 'BHS_SCREEN'
        self.household_member_female.save()
        self.household_member_male.save()
        EnrollmentChecklistFactory(
            household_member=self.household_member_female,
            gender='F',
            citizen='Yes',
            dob=female_dob,
            guardian='No',
            initials=self.household_member_female.initials,
            part_time_resident='Yes')
        EnrollmentChecklistFactory(
            household_member=self.household_member_male,
            gender='M',
            citizen='Yes',
            dob=male_dob,
            guardian='No',
            initials=self.household_member_male.initials,
            part_time_resident='Yes')
        subject_consent_female = SubjectConsentFactory(household_member=self.household_member_female, study_site=study_site, gender='F', dob=female_dob, first_name=female_first_name, initials=female_initials)
        subject_consent_male = SubjectConsentFactory(household_member=self.household_member_male, study_site=study_site, gender='M', dob=male_dob, first_name=male_first_name, initials=male_initials)

        self.registered_subject_female = RegisteredSubject.objects.get(subject_identifier=subject_consent_female.subject_identifier)
        self.registered_subject_male = RegisteredSubject.objects.get(subject_identifier=subject_consent_male.subject_identifier)
        self.appointment_female = Appointment.objects.get(registered_subject=self.registered_subject_female)
        self.subject_visit_female = SubjectVisitFactory(appointment=self.appointment_female, household_member=self.household_member_female)
        self.appointment_male = Appointment.objects.get(registered_subject=self.registered_subject_male)
        self.subject_visit_male = SubjectVisitFactory(appointment=self.appointment_male, household_member=self.household_member_male)

    def new_metadata_is_not_keyed(self):
        self.assertEquals(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, appointment=self.subject_visit_male.appointment).count(), 0)
        self.assertEquals(RequisitionMetaData.objects.filter(entry_status=KEYED, appointment=self.subject_visit_male.appointment).count(), 0)

    def test_hiv_car_adherence_and_pima1(self):
        """If POS and not on arv and no doc evidence, Pima required.

        Models:
            * HivCareAdherence
            * HivResult
        """
        self.subject_visit_male.delete()
        self.assertEqual(ScheduledEntryMetaData.objects.filter(appointment=self.appointment_male).count(), 0)
        self.subject_visit_male = SubjectVisitFactory(appointment=self.appointment_male, household_member=self.household_member_male)
        self.check_male_registered_subject_rule_groups(self.subject_visit_male)

        hiv_car_adherence_options = {}
        hiv_car_adherence_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivcareadherence',
            appointment=self.subject_visit_male.appointment)
        pima_options = {}
        pima_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pima',
            appointment=self.subject_visit_male.appointment)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **hiv_car_adherence_options).count(), 1)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **pima_options).count(), 1)

        # add HivCarAdherence,
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male,
            first_positive=None,
            medical_care='No',
            ever_recommended_arv='No',
            ever_taken_arv='Yes',
            on_arv='No',
            arv_evidence='No',  # this is the rule field
            )
        # said they have taken ARV so not required
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **pima_options).count(), 1)

    def test_hiv_car_adherence_and_pima2(self):
        """If POS and on arv and have doc evidence, Pima not required.

        Models:
            * HivCareAdherence
            * HivResult
        """
        self.subject_visit_female.delete()
        self.subject_visit_female = SubjectVisitFactory(appointment=self.appointment_female, household_member=self.household_member_female)
        self.check_male_registered_subject_rule_groups(self.subject_visit_female)

        hiv_car_adherence_options = {}
        hiv_car_adherence_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivcareadherence',
            appointment=self.subject_visit_female.appointment)
        pima_options = {}
        pima_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pima',
            appointment=self.subject_visit_female.appointment)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **hiv_car_adherence_options).count(), 1)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **pima_options).count(), 1)

        # add HivCarAdherence,
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_female,
            first_positive=None,
            medical_care='No',
            ever_recommended_arv='No',
            ever_taken_arv='No',
            on_arv='Yes',
            arv_evidence='Yes',  # this is the rule field
            )

        # on art so no need for CD4
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **pima_options).count(), 1)

    def test_hiv_car_adherence_and_pima3(self):
        """If POS and on arv but do not have doc evidence, Pima required.

        Models:
            * HivCareAdherence
            * HivResult
        """
        self.subject_visit_male.delete()
        self.subject_visit_male = SubjectVisitFactory(appointment=self.appointment_male, household_member=self.household_member_male)
        self.check_male_registered_subject_rule_groups(self.subject_visit_male)

        hiv_car_adherence_options = {}
        hiv_car_adherence_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivcareadherence',
            appointment=self.subject_visit_male.appointment)
        pima_options = {}
        pima_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pima',
            appointment=self.subject_visit_male.appointment)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **hiv_car_adherence_options).count(), 1)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **pima_options).count(), 1)

        # add HivCarAdherence,
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male,
            first_positive=None,
            medical_care='No',
            ever_recommended_arv='No',
            ever_taken_arv='No',
            on_arv='Yes',
            arv_evidence='No',  # this is the rule field
            )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **pima_options).count(), 1)

    def test_hiv_care_adherence_and_pima4(self):
        """If POS and not on arv but have doc evidence, Pima required.

        Models:
            * HivCareAdherence
            * HivResult
        """
        self.subject_visit_male.delete()
        self.subject_visit_male = SubjectVisitFactory(appointment=self.appointment_male, household_member=self.household_member_male)        
        self.check_male_registered_subject_rule_groups(self.subject_visit_male)

        hiv_car_adherence_options = {}
        hiv_car_adherence_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivcareadherence',
            appointment=self.subject_visit_male.appointment)
        pima_options = {}
        pima_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pima',
            appointment=self.subject_visit_male.appointment)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **hiv_car_adherence_options).count(), 1)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **pima_options).count(), 1)

        # add HivCarAdherence,
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male,
            first_positive=None,
            medical_care='No',
            ever_recommended_arv='No',
            ever_taken_arv='No',
            on_arv='No',
            arv_evidence='Yes',  # this is the rule field
            )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **pima_options).count(), 1)

    def test_not_known_pos_runs_hiv_and_cd4(self):
        """If not a known POS, requires HIV and CD4 (until today's result is known)."""
        self.subject_visit_male.delete()
        self.subject_visit_male = SubjectVisitFactory(appointment=self.appointment_male, household_member=self.household_member_male)
        self.check_male_registered_subject_rule_groups(self.subject_visit_male)

        hiv_test_review_options = {}
        hiv_test_review_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivtestreview',
            appointment=self.subject_visit_male.appointment)

        pima_options = {}
        pima_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pima',
            appointment=self.subject_visit_male.appointment)

        hiv_result_options = {}
        hiv_result_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivresult',
            appointment=self.subject_visit_male.appointment)

        # add HivTestReview,
        hiv_test_review = HivTestReview.objects.create(
            subject_visit=self.subject_visit_male,
            hiv_test_date=datetime.today() - timedelta(days=50),
            recorded_hiv_result='NEG',
            )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_test_review_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **hiv_result_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **pima_options).count(), 1)

        hiv_test_review.recorded_hiv_result = 'IND'
        hiv_test_review.save()
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_test_review_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **hiv_result_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **pima_options).count(), 1)

        hiv_test_review.recorded_hiv_result = 'UNK'
        hiv_test_review.save()
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_test_review_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **hiv_result_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **pima_options).count(), 1)

    def test_known_pos_completes_hiv_care_adherence(self):
        """If known POS (not including today's test), requires hiv_care_adherence."""
        self.subject_visit_male.delete()
        self.subject_visit_male = SubjectVisitFactory(appointment=self.appointment_male, household_member=self.household_member_male)
        self.check_male_registered_subject_rule_groups(self.subject_visit_male)

        hiv_test_review_options = {}
        hiv_test_review_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivtestreview',
            appointment=self.subject_visit_male.appointment)

        hiv_care_adherence_options = {}
        hiv_care_adherence_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivcareadherence',
            appointment=self.subject_visit_male.appointment)

        # add HivTestReview,
        HivTestReview.objects.create(
            subject_visit=self.subject_visit_male,
            hiv_test_date=datetime.today() - timedelta(days=50),
            recorded_hiv_result='POS',
            )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_test_review_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **hiv_care_adherence_options).count(), 1)

    def test_known_neg_does_not_complete_hiv_care_adherence(self):
        """If known POS (not including today's test), requires hiv_care_adherence."""
        self.subject_visit_male.delete()
        self.subject_visit_male = SubjectVisitFactory(appointment=self.appointment_male, household_member=self.household_member_male)
        self.check_male_registered_subject_rule_groups(self.subject_visit_male)

        hiv_test_history_options = {}
        hiv_test_history_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivtestinghistory',
            appointment=self.subject_visit_male.appointment)

        hiv_test_review_options = {}
        hiv_test_review_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivtestreview',
            appointment=self.subject_visit_male.appointment)

        hiv_care_adherence_options = {}
        hiv_care_adherence_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivcareadherence',
            appointment=self.subject_visit_male.appointment)

        # add HivTestHistory,
        hiv_testing_history = HivTestingHistoryFactory(subject_visit=self.subject_visit_male)
        hiv_testing_history.save()
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_test_history_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **hiv_test_review_options).count(), 1)
        # add HivTestReview,
        hiv_care_adherence = HivTestReview.objects.create(
            subject_visit=self.subject_visit_male,
            hiv_test_date=datetime.today() - timedelta(days=50),
            recorded_hiv_result='NEG',
            )
        #hiv_care_adherence.save()

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_test_review_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **hiv_care_adherence_options).count(), 1)

    def test_known_neg_requires_hiv_test_today(self):
        """If previous result is NEG, need to test today (HivResult).

        See rule_groups.ReviewNotPositiveRuleGroup
        """
        self.subject_visit_male.delete()
        self.subject_visit_male = SubjectVisitFactory(appointment=self.appointment_male, household_member=self.household_member_male)
        self.check_male_registered_subject_rule_groups(self.subject_visit_male)

        hiv_test_review_options = {}
        hiv_test_review_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivtestreview',
            appointment=self.subject_visit_male.appointment)

        hiv_result_options = {}
        hiv_result_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivresult',
            appointment=self.subject_visit_male.appointment)

        # add HivTestReview,
        HivTestReview.objects.create(
            subject_visit=self.subject_visit_male,
            hiv_test_date=datetime.today() - timedelta(days=50),
            recorded_hiv_result='NEG',
            )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_test_review_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **hiv_result_options).count(), 1)

    def test_known_pos_does_not_require_hiv_test_today(self):
        """If previous result is POS, do not need to test today (HivResult).

        See rule_groups.ReviewNotPositiveRuleGroup
        """
        self.subject_visit_male.delete()
        self.subject_visit_male = SubjectVisitFactory(appointment=self.appointment_male, household_member=self.household_member_male)
#         for entry in ScheduledEntryMetaData.objects.filter(appointment=self.subject_visit_male.appointment):
#             print '{0}, {1}'.format(entry.entry, entry.entry_status)
        self.check_male_registered_subject_rule_groups(self.subject_visit_male)

        hiv_test_review_options = {}
        hiv_test_review_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivtestreview',
            appointment=self.subject_visit_male.appointment)

        hiv_result_options = {}
        hiv_result_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivresult',
            appointment=self.subject_visit_male.appointment)

        # add HivTestReview,
        HivTestReview.objects.create(
            subject_visit=self.subject_visit_male,
            hiv_test_date=datetime.today() - timedelta(days=50),
            recorded_hiv_result='POS',
            )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_test_review_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **hiv_result_options).count(), 1)

    def test_known_pos_stigma_forms(self):
        """If known posetive, test stigma forms
        """
        self.subject_visit_female.delete()
        self.subject_visit_female = SubjectVisitFactory(appointment=self.appointment_female, household_member=self.household_member_female)
        self.check_male_registered_subject_rule_groups(self.subject_visit_female)

        hiv_test_history_options = {}
        hiv_test_history_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivtestinghistory',
            appointment=self.subject_visit_female.appointment)

        stigma_options = {}
        stigma_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='stigma',
            appointment=self.subject_visit_female.appointment)

        stigmaopinion_options = {}
        stigmaopinion_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='stigmaopinion',
            appointment=self.subject_visit_female.appointment)

        hiv_testing_history = HivTestingHistoryFactory(subject_visit=self.subject_visit_female)
        hiv_testing_history.save()

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_test_history_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **stigma_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **stigmaopinion_options).count(), 1)

    def test_hiv_tested_forms(self):
        """If known posetive, test hivtested forms
        """
        self.subject_visit_female.delete()
        self.subject_visit_female = SubjectVisitFactory(appointment=self.appointment_female, household_member=self.household_member_female)
        self.check_male_registered_subject_rule_groups(self.subject_visit_female)

        hiv_test_history_options = {}
        hiv_test_history_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivtestinghistory',
            appointment=self.subject_visit_female.appointment)

        hiv_untested_options = {}
        hiv_untested_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivuntested',
            appointment=self.subject_visit_female.appointment)

        hiv_tested_options = {}
        hiv_tested_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivtested',
            appointment=self.subject_visit_female.appointment)

        hiv_testing_history = HivTestingHistoryFactory(subject_visit=self.subject_visit_female)
        hiv_testing_history.save()
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_test_history_options).count(), 1),
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **hiv_tested_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **hiv_untested_options).count(), 1)

        hiv_testing_history.has_tested = 'No'
        hiv_testing_history.save()
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **hiv_untested_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **hiv_tested_options).count(), 1)

    def test_cancer_hearattack_tb_forms(self):
        """Medical diagnoses forms
        """
        self.subject_visit_female.delete()
        self.subject_visit_female = SubjectVisitFactory(appointment=self.appointment_female, household_member=self.household_member_female)
        self.check_male_registered_subject_rule_groups(self.subject_visit_female)

        heartattack_options = {}
        heartattack_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='heartattack',
            appointment=self.subject_visit_female.appointment)

        cancer_options = {}
        cancer_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='cancer',
            appointment=self.subject_visit_female.appointment)

        tbsymptoms_options = {}
        tbsymptoms_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='tbsymptoms',
            appointment=self.subject_visit_female.appointment)

        medicaldiagnoses_options = {}
        medicaldiagnoses_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='medicaldiagnoses',
            appointment=self.subject_visit_female.appointment)

        diagnoses = Diagnoses.objects.create(name = 'Heart Disease or Stroke')
        medical_diagnoses = MedicalDiagnosesFactory(subject_visit=self.subject_visit_female)
        medical_diagnoses.diagnoses.add(diagnoses)
        medical_diagnoses.save()
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **medicaldiagnoses_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **heartattack_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **cancer_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **tbsymptoms_options).count(), 1)

        medical_diagnoses.diagnoses.remove(diagnoses)
        diagnoses.name = 'Cancer'
        diagnoses.save()
        medical_diagnoses.diagnoses.add(diagnoses)
        medical_diagnoses.save()
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **heartattack_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **cancer_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **tbsymptoms_options).count(), 1)

        medical_diagnoses.diagnoses.remove(diagnoses)
        diagnoses.name = 'Tubercolosis'
        diagnoses.save()
        medical_diagnoses.diagnoses.add(diagnoses)
        medical_diagnoses.save()
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **heartattack_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **cancer_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **tbsymptoms_options).count(), 1)

    def test_known_pos_on_art_no_doc_requires_cd4_only(self):
        """If previous result is POS on art but no evidence, need to run CD4 (Pima).

        See rule_groups.ReviewNotPositiveRuleGroup and
        """
        self.subject_visit_male.delete()
        self.subject_visit_male = SubjectVisitFactory(appointment=self.appointment_male, household_member=self.household_member_male)
        self.check_male_registered_subject_rule_groups(self.subject_visit_male)

        hiv_test_review_options = {}
        hiv_test_review_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivtestreview',
            appointment=self.subject_visit_male.appointment)

        hiv_result_options = {}
        hiv_result_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivresult',
            appointment=self.subject_visit_male.appointment)

        pima_options = {}
        pima_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pima',
            appointment=self.subject_visit_male.appointment)

        hiv_care_adherence_options = {}
        hiv_care_adherence_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivcareadherence',
            appointment=self.subject_visit_male.appointment)

        # add HivTestReview,
        HivTestReview.objects.create(
            subject_visit=self.subject_visit_male,
            hiv_test_date=datetime.today() - timedelta(days=50),
            recorded_hiv_result='POS',
            )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **hiv_care_adherence_options).count(), 1)

        # add HivCareAdherence,
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male,
            first_positive=None,
            medical_care='No',
            ever_recommended_arv='No',
            ever_taken_arv='No',
            on_arv='Yes',
            arv_evidence='No',  # this is the rule field
            )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_test_review_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_care_adherence_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **hiv_result_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **pima_options).count(), 1)

    def test_hiv_care_adherance_for_verbal_posetive_only(self):
        """HivCareAdharance form should be made available any verbal positive,
            not considering availability or lack thereof documentation.
        """
        self.subject_visit_male.delete()
        self.subject_visit_male = SubjectVisitFactory(appointment=self.appointment_male, household_member=self.household_member_male)
        self.check_male_registered_subject_rule_groups(self.subject_visit_male)

        HivTestingHistory.objects.create(
            subject_visit=self.subject_visit_male,
            has_tested='Yes',
            when_hiv_test='1 to 5 months ago',
            has_record='No',
            verbal_hiv_result='POS',
            other_record='No'
            )

        hiv_care_adherence_options = {}
        hiv_care_adherence_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivcareadherence',
            appointment=self.subject_visit_male.appointment)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **hiv_care_adherence_options).count(), 1)

    def test_known_pos_on_art_with_doc_requires_cd4_only(self):
        """If previous result is POS on art with doc evidence, do not run HIV or CD4.

        See rule_groups.ReviewNotPositiveRuleGroup and
        """
        self.subject_visit_male.delete()
        self.subject_visit_male = SubjectVisitFactory(appointment=self.appointment_male, household_member=self.household_member_male)
        self.check_male_registered_subject_rule_groups(self.subject_visit_male)

        hiv_test_review_options = {}
        hiv_test_review_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivtestreview',
            appointment=self.subject_visit_male.appointment)

        hiv_result_options = {}
        hiv_result_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivresult',
            appointment=self.subject_visit_male.appointment)

        pima_options = {}
        pima_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pima',
            appointment=self.subject_visit_male.appointment)

        hiv_care_adherence_options = {}
        hiv_care_adherence_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivcareadherence',
            appointment=self.subject_visit_male.appointment)

        # add HivTestReview,
        HivTestReview.objects.create(
            subject_visit=self.subject_visit_male,
            hiv_test_date=datetime.today() - timedelta(days=50),
            recorded_hiv_result='POS',
            )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **hiv_care_adherence_options).count(), 1)

        # add HivCareAdherence,
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male,
            first_positive=None,
            medical_care='No',
            ever_recommended_arv='No',
            ever_taken_arv='No',
            on_arv='Yes',
            arv_evidence='Yes',  # this is the rule field
            )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_test_review_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_care_adherence_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **hiv_result_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **pima_options).count(), 1)

    def test_known_pos_no_art_but_has_doc_requires_cd4_only(self):
        """If previous result is POS on art but no evidence, need to run CD4 (Pima).

        This is a defaulter

        See rule_groups.ReviewNotPositiveRuleGroup and
        """
        self.subject_visit_male.delete()
        self.subject_visit_male = SubjectVisitFactory(appointment=self.appointment_male, household_member=self.household_member_male)
        self.check_male_registered_subject_rule_groups(self.subject_visit_male)

        hiv_test_review_options = {}
        hiv_test_review_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivtestreview',
            appointment=self.subject_visit_male.appointment)

        hiv_result_options = {}
        hiv_result_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivresult',
            appointment=self.subject_visit_male.appointment)

        pima_options = {}
        pima_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pima',
            appointment=self.subject_visit_male.appointment)

        hiv_care_adherence_options = {}
        hiv_care_adherence_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivcareadherence',
            appointment=self.subject_visit_male.appointment)

        # add HivTestReview,
        HivTestReview.objects.create(
            subject_visit=self.subject_visit_male,
            hiv_test_date=datetime.today() - timedelta(days=50),
            recorded_hiv_result='POS',
            )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **hiv_care_adherence_options).count(), 1)

        # add HivCareAdherence,
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male,
            first_positive=None,
            medical_care='No',
            ever_recommended_arv='No',
            ever_taken_arv='No',
            on_arv='No',
            arv_evidence='Yes',  # this is the rule field
            )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_test_review_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_care_adherence_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **hiv_result_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **pima_options).count(), 1)

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

        if subject_visit == self.subject_visit_male:
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

    def test_elisaresult_behaves_like_todayhivresult(self):
        """when an elisa result is keyed in, a +ve result should result in RBD and VL
            being REQUIRED just like Today's HivResult
        """
        self.subject_visit_male.delete()
        self.subject_visit_male = SubjectVisitFactory(appointment=self.appointment_male, household_member=self.household_member_male)
        self.check_male_registered_subject_rule_groups(self.subject_visit_male)

        hiv_test_review_options = {}
        hiv_test_review_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivtestreview',
            appointment=self.subject_visit_male.appointment)

        hiv_result_options = {}
        hiv_result_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivresult',
            appointment=self.subject_visit_male.appointment)

        elisa_hiv_result_options = {}
        elisa_hiv_result_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='elisahivresult',
            appointment=self.subject_visit_male.appointment)

        research_blood_draw_options = {}
        research_blood_draw_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Research Blood Draw',
            appointment=self.subject_visit_male.appointment)

        viral_load_options = {}
        viral_load_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Viral Load',
            appointment=self.subject_visit_male.appointment)

        # add HivTestReview,
        HivTestReview.objects.create(
            subject_visit=self.subject_visit_male,
            hiv_test_date=datetime.today() - timedelta(days=50),
            recorded_hiv_result='NEG',
            )
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **hiv_result_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **elisa_hiv_result_options).count(), 1)

        aliquot_type = AliquotType.objects.all()[0]
        site = StudySite.objects.all()[0]
        microtube_panel = Panel.objects.get(name='Microtube')
        micro_tube = SubjectRequisitionFactory(subject_visit=self.subject_visit_male, panel=microtube_panel, aliquot_type=aliquot_type, site=site)
        HivResult.objects.create(
             subject_visit=self.subject_visit_male,
             hiv_result='IND',
             report_datetime=datetime.today(),
             insufficient_vol='No'
            )
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **elisa_hiv_result_options).count(), 1)

        elisa_panel = Panel.objects.get(name='ELISA')
        elisa = SubjectRequisitionFactory(subject_visit=self.subject_visit_male, panel=elisa_panel, aliquot_type=aliquot_type, site=site)
        ElisaHivResult.objects.create(
             subject_visit=self.subject_visit_male,
             hiv_result='POS',
             hiv_result_datetime=datetime.today(),
            )
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **elisa_hiv_result_options).count(), 1)

        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **viral_load_options).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **research_blood_draw_options).count(), 1)

#     def test_enter_out_of_order(self):
#         """Add models out of order.
# 
#         See rule_groups.ReviewNotPositiveRuleGroup and
#         """
#         self.subject_visit_male.delete()
#         self.subject_visit_male = SubjectVisitFactory(appointment=self.appointment_male, household_member=self.household_member_male)
# 
#         hiv_test_review_options = {}
#         hiv_test_review_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='hivtestreview',
#             appointment=self.subject_visit_male.appointment)
# 
#         hiv_result_options = {}
#         hiv_result_options.update(
#             {'entry__app_label': 'bcpp_subject',
#             'entry__model_name': 'hivresult',
#             'appointment': self.subject_visit_male.appointment})
# 
#         pima_options = {}
#         pima_options.update(
#             {'entry__app_label': 'bcpp_subject',
#             'entry__model_name': 'pima',
#             'appointment': self.subject_visit_male.appointment})
# 
#         hiv_care_adherence_options = {}
#         hiv_care_adherence_options.update(
#             {'entry__app_label': 'bcpp_subject',
#             'entry__model_name': 'hivcareadherence',
#             'appointment': self.subject_visit_male.appointment})
# 
#         # add HivCareAdherence, out of order ...
#         hiv_care_adherence = HivCareAdherence.objects.create(
#             subject_visit=self.subject_visit_male,
#             first_positive=None,
#             medical_care='No',
#             ever_recommended_arv='No',
#             ever_taken_arv='No',
#             on_arv='No',
#             arv_evidence='Yes',  # this is the rule field
#             )
# 
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **hiv_test_review_options).count(), 1)
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_care_adherence_options).count(), 1)
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **hiv_result_options).count(), 1)
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **pima_options).count(), 1)
# 
#         # add HivTestReview,
#         hiv_test_review = HivTestReview.objects.create(
#             subject_visit=self.subject_visit_male,
#             hiv_test_date=datetime.today() - timedelta(days=50),
#             recorded_hiv_result='POS',
#             )
# 
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_test_review_options).count(), 1)
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_care_adherence_options).count(), 1)
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **hiv_result_options).count(), 1)
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **pima_options).count(), 1)
# 
#         hiv_test_review.recorded_hiv_result = 'NEG'  # and arv_evidence = 'Yes'
#         hiv_test_review.save()
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_test_review_options).count(), 1)
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_care_adherence_options).count(), 1)
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **hiv_result_options).count(), 1)
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **pima_options).count(), 1)
# 
#         hiv_care_adherence.arv_evidence = 'No'  # and recorded_hiv_result = 'NEG'
#         hiv_care_adherence.save()
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_test_review_options).count(), 1)
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_care_adherence_options).count(), 1)
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **hiv_result_options).count(), 1)
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **pima_options).count(), 1)
# 
#         hiv_test_review.recorded_hiv_result = 'IND'  # and arv_evidence = 'No'
#         hiv_test_review.save()
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_test_review_options).count(), 1)
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_care_adherence_options).count(), 1)
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **hiv_result_options).count(), 1)
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **pima_options).count(), 1)
# 
#         hiv_care_adherence.arv_evidence = 'No'  # and recorded_hiv_result = 'IND'
#         hiv_test_review.save()
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_test_review_options).count(), 1)
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_care_adherence_options).count(), 1)
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **hiv_result_options).count(), 1)
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **pima_options).count(), 1)
