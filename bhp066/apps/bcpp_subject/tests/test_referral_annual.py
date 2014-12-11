from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

from edc.map.classes import Mapper, site_mappers

from apps.bcpp_lab.models import AliquotType, Panel
from apps.bcpp_lab.tests.factories import SubjectRequisitionFactory

from ..classes import SubjectReferralHelper

from .base_scheduled_model_test_case import BaseScheduledModelTestCase
from .factories import (
    SubjectReferralFactory, ReproductiveHealthFactory,
    HivCareAdherenceFactory, HivResultFactory, CircumcisionFactory,
    PimaFactory, HivTestReviewFactory, HivTestingHistoryFactory, TbSymptomsFactory,
    HivResultDocumentationFactory)
from edc.entry_meta_data.models.scheduled_entry_meta_data import ScheduledEntryMetaData
from edc.constants import NOT_REQUIRED, REQUIRED
from edc.entry_meta_data.models.requisition_meta_data import RequisitionMetaData
from edc.export.models.export_transaction import ExportTransaction
from apps.bcpp_subject.tests.factories.subject_locator_factory import SubjectLocatorFactory
from apps.bcpp_household.constants import BASELINE_SURVEY_SLUG
from apps.bcpp_survey.models import Survey


# class TestPlotMapper(Mapper):
#     map_area = 'test_community8'
#     map_code = '11'  # has to be a code in the clinic days dictionary
#     regions = []
#     sections = []
#     landmarks = []
#     gps_center_lat = -25.033192
#     gps_center_lon = 25.747139
#     radius = 5.5
#     location_boundary = ()
# 
# site_mappers.register(TestPlotMapper)


class TestReferralAnnual(BaseScheduledModelTestCase):

    def startup(self):
        super(TestReferralAnnual, self).startup()
        SubjectLocatorFactory(subject_visit=self.subject_visit_male)
        SubjectLocatorFactory(subject_visit=self.subject_visit_female)

    def tests_hiv_result4a(self):
        """Other record confirms a verbal positive as evidence of HIV infection not on ART."""
        from ..classes import SubjectStatusHelper
        site_mappers.current_mapper.intervention = True
        print Survey.objects.current_survey()
        self.startup()
        report_datetime = datetime.today()
        today_date = date.today()
        last_year_date = today_date - timedelta(days=365)
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='POS', has_record='No', other_record='Yes')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='No', arv_evidence='No')
        hiv_result_documentation = HivResultDocumentationFactory(subject_visit=self.subject_visit_male, result_recorded='POS', result_date=last_year_date, result_doc_type='ART Prescription')
        subject_referral = SubjectStatusHelper(self.subject_visit_male)
        self.assertEqual('POS', subject_referral.hiv_result)
        self.assertFalse(subject_referral.new_pos)
        self.assertTrue(subject_referral.on_art is False)
        self.assertTrue(ScheduledEntryMetaData.objects.filter(
            appointment=self.subject_visit_male.appointment,
            entry__model_name='hivresult',
            entry_status=REQUIRED).count() == 1)

        self.assertTrue(ScheduledEntryMetaData.objects.filter(
            appointment=self.subject_visit_male.appointment,
            entry__model_name='pima',
            entry_status=REQUIRED).count() == 1)

    def tests_hiv_result4b(self):
        """Other record confirms a verbal positive as evidence of HIV infection not on ART."""
        from ..classes import SubjectStatusHelper
        site_mappers.current_mapper.intervention = False
        print Survey.objects.current_survey()
        self.startup()
        report_datetime = datetime.today()
        today_date = date.today()
        last_year_date = today_date - timedelta(days=365)
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='POS', has_record='No', other_record='Yes')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='No', arv_evidence='No')
        hiv_result_documentation = HivResultDocumentationFactory(subject_visit=self.subject_visit_male, result_recorded='POS', result_date=last_year_date, result_doc_type='ART Prescription')
        subject_referral = SubjectStatusHelper(self.subject_visit_male)
        self.assertEqual('POS', subject_referral.hiv_result)
        self.assertFalse(subject_referral.new_pos)
        self.assertTrue(subject_referral.on_art is False)
        self.assertTrue(ScheduledEntryMetaData.objects.filter(
            appointment=self.subject_visit_male.appointment,
            entry__model_name='hivresult',
            entry_status=REQUIRED).count() == 1)

        self.assertTrue(ScheduledEntryMetaData.objects.filter(
            appointment=self.subject_visit_male.appointment,
            entry__model_name='pima',
            entry_status=NOT_REQUIRED).count() == 1)
