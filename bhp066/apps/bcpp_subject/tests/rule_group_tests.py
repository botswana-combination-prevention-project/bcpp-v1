from datetime import datetime, timedelta

from django.core.management import call_command
from django.db.models import get_app, get_models
from django.test import TestCase

from edc.core.bhp_content_type_map.classes import ContentTypeMapHelper
from edc.core.bhp_content_type_map.models import ContentTypeMap
from edc.core.bhp_variables.tests.factories import StudySpecificFactory, StudySiteFactory

from edc.map.classes import Mapper, site_mappers
from edc.subject.appointment.models import Appointment
from edc.subject.appointment.tests.factories import ConfigurationFactory
from edc.subject.consent.tests.factories import ConsentCatalogueFactory
from edc.subject.entry.models import Entry
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.registration.models import RegisteredSubject
from edc.subject.rule_groups.classes import site_rule_groups
from edc.subject.visit_schedule.models import VisitDefinition, MembershipForm, ScheduleGroup
from edc.subject.visit_schedule.tests.factories import MembershipFormFactory, ScheduleGroupFactory, VisitDefinitionFactory
from edc.subject.visit_schedule.classes import site_visit_schedules
from edc.subject.entry.models import ScheduledEntryMetaData

from apps.bcpp_household.models import Plot, Household, HouseholdStructure
from apps.bcpp_household.tests.factories import PlotFactory
from apps.bcpp_household_member.tests.factories import HouseholdMemberFactory
from apps.bcpp_survey.tests.factories import SurveyFactory

from ..models import HivCareAdherence, HivTestingHistory, HivTestReview
from .factories import SubjectConsentFactory, SubjectVisitFactory, HivCareAdherenceFactory


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


class RuleGroupTests(TestCase):

    app_label = 'bcpp_subject'
    community = 'test_community9'

    def setUp(self):

        content_type_map_helper = ContentTypeMapHelper()
        content_type_map_helper.populate()
        content_type_map_helper.sync()

        study_specific = StudySpecificFactory()
        StudySiteFactory()
        ConfigurationFactory()

        content_type_map = ContentTypeMap.objects.get(content_type__model='SubjectConsent'.lower())
        ConsentCatalogueFactory(
            name=self.app_label,
            consent_type='study',
            content_type_map=content_type_map,
            version=1,
            start_datetime=study_specific.study_start_datetime,
            end_datetime=datetime(datetime.today().year + 5, 1, 1),
            add_for_app=self.app_label)

        site_visit_schedules.autodiscover()
        visit_schedule = site_visit_schedules.get_visit_schedule('bcpp_subject')
        visit_schedule.build()

        site_rule_groups.autodiscover()

        self.survey = SurveyFactory()

        plot = PlotFactory(community=self.community, household_count=1, status='occupied')

        household_structure = HouseholdStructure.objects.get(household__plot=plot)
        HouseholdMemberFactory(household_structure=household_structure)
        HouseholdMemberFactory(household_structure=household_structure)
        HouseholdMemberFactory(household_structure=household_structure)

        self.household_member_female = HouseholdMemberFactory(household_structure=household_structure, gender='F')
        self.household_member_male = HouseholdMemberFactory(household_structure=household_structure, gender='M')
        self.household_member_female.eligible_member = True
        self.household_member_male.eligible_member = True
        self.household_member_female.eligible_subject = True
        self.household_member_male.eligible_subject = True
        self.household_member_female.save()
        self.household_member_male.save()

        subject_consent_female = SubjectConsentFactory(household_member=self.household_member_female, gender='F')
        subject_consent_male = SubjectConsentFactory(household_member=self.household_member_male, gender='M')

        self.registered_subject_female = RegisteredSubject.objects.get(subject_identifier=subject_consent_female.subject_identifier)
        self.registered_subject_male = RegisteredSubject.objects.get(subject_identifier=subject_consent_male.subject_identifier)
        self.appointment_female = Appointment.objects.get(registered_subject=self.registered_subject_female)
        self.subject_visit_female = SubjectVisitFactory(appointment=self.appointment_female, household_member=self.household_member_female)
        self.appointment_male = Appointment.objects.get(registered_subject=self.registered_subject_male)
        self.subject_visit_male = SubjectVisitFactory(appointment=self.appointment_male, household_member=self.household_member_male)

    def test_hiv_car_adherence_and_pima1(self):
        """If POS and not on arv and no doc evidence, Pima required.

        Models:
            * HivCareAdherence
            * HivResult
        """
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

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NEW', **hiv_car_adherence_options).count(), 1)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NEW', **pima_options).count(), 1)

        # add HivCarAdherence,
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male,
            first_positive=None,
            medical_care='No',
            ever_recommended_arv='No',
            arv_naive='Yes',
            on_arv='No',
            arv_evidence='No',  # this is the rule field
            )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NEW', **pima_options).count(), 1)

    def test_hiv_car_adherence_and_pima2(self):
        """If POS and on arv and have doc evidence, Pima not required.

        Models:
            * HivCareAdherence
            * HivResult
        """
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

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NEW', **hiv_car_adherence_options).count(), 1)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NEW', **pima_options).count(), 1)

        # add HivCarAdherence,
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male,
            first_positive=None,
            medical_care='No',
            ever_recommended_arv='No',
            arv_naive='No',
            on_arv='Yes',
            arv_evidence='Yes',  # this is the rule field
            )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NOT_REQUIRED', **pima_options).count(), 1)

    def test_hiv_car_adherence_and_pima3(self):
        """If POS and on arv but do not have doc evidence, Pima required.

        Models:
            * HivCareAdherence
            * HivResult
        """
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

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NEW', **hiv_car_adherence_options).count(), 1)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NEW', **pima_options).count(), 1)

        # add HivCarAdherence,
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male,
            first_positive=None,
            medical_care='No',
            ever_recommended_arv='No',
            arv_naive='No',
            on_arv='Yes',
            arv_evidence='No',  # this is the rule field
            )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NEW', **pima_options).count(), 1)

    def test_hiv_care_adherence_and_pima4(self):
        """If POS and not on arv but have doc evidence, Pima required.

        Models:
            * HivCareAdherence
            * HivResult
        """
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

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NEW', **hiv_car_adherence_options).count(), 1)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NEW', **pima_options).count(), 1)

        # add HivCarAdherence,
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male,
            first_positive=None,
            medical_care='No',
            ever_recommended_arv='No',
            arv_naive='No',
            on_arv='No',
            arv_evidence='Yes',  # this is the rule field
            )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NOT_REQUIRED', **pima_options).count(), 1)

    def test_not_known_pos_runs_hiv_and_cd4(self):
        """If not a known POS, requires HIV and CD4 (until today's result is known)."""
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

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='KEYED', **hiv_test_review_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NEW', **hiv_result_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NEW', **pima_options).count(), 1)

        hiv_test_review.recorded_hiv_result = 'IND'
        hiv_test_review.save()
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='KEYED', **hiv_test_review_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NEW', **hiv_result_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NEW', **pima_options).count(), 1)

        hiv_test_review.recorded_hiv_result = 'UNK'
        hiv_test_review.save()
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='KEYED', **hiv_test_review_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NEW', **hiv_result_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NEW', **pima_options).count(), 1)

    def test_known_pos_completes_hiv_care_adherence(self):
        """If known POS (not including today's test), requires hiv_care_adherence."""
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

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='KEYED', **hiv_test_review_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NEW', **hiv_care_adherence_options).count(), 1)

    def test_known_neg_does_not_complete_hiv_care_adherence(self):
        """If known POS (not including today's test), requires hiv_care_adherence."""
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
            recorded_hiv_result='NEG',
            )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='KEYED', **hiv_test_review_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NOT_REQUIRED', **hiv_care_adherence_options).count(), 1)

    def test_known_neg_requires_hiv_test_today(self):
        """If previous result is NEG, need to test today (HivResult).

        See rule_groups.ReviewNotPositiveRuleGroup
        """
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

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='KEYED', **hiv_test_review_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NEW', **hiv_result_options).count(), 1)

    def test_known_pos_does_not_require_hiv_test_today(self):
        """If previous result is POS, do not need to test today (HivResult).

        See rule_groups.ReviewNotPositiveRuleGroup
        """
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

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='KEYED', **hiv_test_review_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NOT_REQUIRED', **hiv_result_options).count(), 1)

    def test_known_pos_on_art_no_doc_requires_cd4_only(self):
        """If previous result is POS on art but no evidence, need to run CD4 (Pima).

        See rule_groups.ReviewNotPositiveRuleGroup and
        """
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

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NEW', **hiv_care_adherence_options).count(), 1)

        # add HivCareAdherence,
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male,
            first_positive=None,
            medical_care='No',
            ever_recommended_arv='No',
            arv_naive='No',
            on_arv='Yes',
            arv_evidence='No',  # this is the rule field
            )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='KEYED', **hiv_test_review_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='KEYED', **hiv_care_adherence_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NOT_REQUIRED', **hiv_result_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NEW', **pima_options).count(), 1)

    def test_known_pos_on_art_with_doc_requires_cd4_only(self):
        """If previous result is POS on art with doc evidence, do not run HIV or CD4.

        See rule_groups.ReviewNotPositiveRuleGroup and
        """
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

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NEW', **hiv_care_adherence_options).count(), 1)

        # add HivCareAdherence,
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male,
            first_positive=None,
            medical_care='No',
            ever_recommended_arv='No',
            arv_naive='No',
            on_arv='Yes',
            arv_evidence='Yes',  # this is the rule field
            )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='KEYED', **hiv_test_review_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='KEYED', **hiv_care_adherence_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NOT_REQUIRED', **hiv_result_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NOT_REQUIRED', **pima_options).count(), 1)

    def test_known_pos_no_art_but_has_doc_requires_cd4_only(self):
        """If previous result is POS on art but no evidence, need to run CD4 (Pima).

        This is a defaulter

        See rule_groups.ReviewNotPositiveRuleGroup and
        """
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

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NEW', **hiv_care_adherence_options).count(), 1)

        # add HivCareAdherence,
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male,
            first_positive=None,
            medical_care='No',
            ever_recommended_arv='No',
            arv_naive='No',
            on_arv='No',
            arv_evidence='Yes',  # this is the rule field
            )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='KEYED', **hiv_test_review_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='KEYED', **hiv_care_adherence_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NOT_REQUIRED', **hiv_result_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NOT_REQUIRED', **pima_options).count(), 1)

    def test_enter_out_of_order(self):
        """Add models out of order.

        See rule_groups.ReviewNotPositiveRuleGroup and
        """
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

        # add HivCareAdherence, out of order ...
        hiv_care_adherence = HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male,
            first_positive=None,
            medical_care='No',
            ever_recommended_arv='No',
            arv_naive='No',
            on_arv='No',
            arv_evidence='Yes',  # this is the rule field
            )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NEW', **hiv_test_review_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='KEYED', **hiv_care_adherence_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NEW', **hiv_result_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NOT_REQUIRED', **pima_options).count(), 1)

        # add HivTestReview,
        hiv_test_review = HivTestReview.objects.create(
            subject_visit=self.subject_visit_male,
            hiv_test_date=datetime.today() - timedelta(days=50),
            recorded_hiv_result='POS',
            )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='KEYED', **hiv_test_review_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='KEYED', **hiv_care_adherence_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NOT_REQUIRED', **hiv_result_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NOT_REQUIRED', **pima_options).count(), 1)

        hiv_test_review.recorded_hiv_result = 'NEG'  # and arv_evidence = 'Yes'
        hiv_test_review.save()
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='KEYED', **hiv_test_review_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='KEYED', **hiv_care_adherence_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NEW', **hiv_result_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NOT_REQUIRED', **pima_options).count(), 1)

        hiv_care_adherence.arv_evidence = 'No'  # and recorded_hiv_result = 'NEG'
        hiv_care_adherence.save()
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='KEYED', **hiv_test_review_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='KEYED', **hiv_care_adherence_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NEW', **hiv_result_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NEW', **pima_options).count(), 1)

        hiv_test_review.recorded_hiv_result = 'IND'  # and arv_evidence = 'No'
        hiv_test_review.save()
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='KEYED', **hiv_test_review_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='KEYED', **hiv_care_adherence_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NEW', **hiv_result_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NEW', **pima_options).count(), 1)

        hiv_care_adherence.arv_evidence = 'No'  # and recorded_hiv_result = 'IND'
        hiv_test_review.save()
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='KEYED', **hiv_test_review_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='KEYED', **hiv_care_adherence_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NEW', **hiv_result_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NEW', **pima_options).count(), 1)
