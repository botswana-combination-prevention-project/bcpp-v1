from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

from edc.map.classes import Mapper, site_mappers
from edc.entry_meta_data.models import ScheduledEntryMetaData, RequisitionMetaData
from edc.constants import REQUIRED, NOT_REQUIRED
from edc.subject.rule_groups.classes import site_rule_groups

from apps.bcpp_lab.models import AliquotType, Panel
from apps.bcpp_lab.tests.factories import SubjectRequisitionFactory

from ..classes import SubjectStatusHelper

from .base_scheduled_model_test_case import BaseScheduledModelTestCase
from .factories import (
    SubjectReferralFactory, ReproductiveHealthFactory,
    HivCareAdherenceFactory, HivResultFactory, CircumcisionFactory,
    PimaFactory, HivTestReviewFactory, HivTestingHistoryFactory, TbSymptomsFactory,
    HivResultDocumentationFactory)


class TestPlotMapper(Mapper):
    map_area = 'test_community81'
    map_code = '097'
    regions = []
    sections = []
    landmarks = []
    gps_center_lat = -25.033192
    gps_center_lon = 25.747139
    radius = 5.5
    location_boundary = ()

site_mappers.register(TestPlotMapper)


class SubjectStatusHelperTests(BaseScheduledModelTestCase):

    community = 'test_community81'

    def tests_hiv_result(self):
        """"""
        subject_status_helper = SubjectStatusHelper(self.subject_visit_male)
        self.assertIsNone(subject_status_helper.hiv_result)
        self.assertIsNone(subject_status_helper.new_pos)

    def tests_hiv_result1(self):
        """"""
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='POS', has_record='No', other_record='No')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='Yes', arv_evidence='No')
        subject_status_helper = SubjectStatusHelper(self.subject_visit_male)
        self.assertIsNone(subject_status_helper.hiv_result)
        self.assertIsNone(subject_status_helper.new_pos)

    def tests_hiv_result2(self):
        """"""
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='POS', has_record='Yes', other_record='No')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='Yes', arv_evidence='No')
        subject_status_helper = SubjectStatusHelper(self.subject_visit_male)
        self.assertIsNone(subject_status_helper.hiv_result)
        self.assertIsNone(subject_status_helper.new_pos)

    def tests_hiv_result2a(self):
        """"""
        today_date = date.today()
        last_year_date = today_date - timedelta(days=365)
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='POS', has_record='Yes', other_record='No')
        HivTestReviewFactory(subject_visit=self.subject_visit_male, recorded_hiv_result='POS', hiv_test_date=last_year_date)
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='Yes', arv_evidence='No')
        subject_status_helper = SubjectStatusHelper(self.subject_visit_male)
        self.assertEquals(subject_status_helper.hiv_result, 'POS')
        self.assertFalse(subject_status_helper.new_pos)

    def tests_hiv_result3(self):
        """"""
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='POS', has_record='No', other_record='Yes')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='Yes', arv_evidence='No')
        subject_status_helper = SubjectStatusHelper(self.subject_visit_male)
        self.assertEquals(subject_status_helper.hiv_result, 'POS')

    def tests_hiv_result4a(self):
        """"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='POS', has_record='No', other_record='No')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='Yes', arv_evidence='No')
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS', hiv_result_datetime=report_datetime)
        subject_status_helper = SubjectStatusHelper(self.subject_visit_male)
        self.assertEquals(subject_status_helper.hiv_result, 'POS')

    def tests_hiv_result5(self):
        """"""
        result_date = datetime(2014,2,9)
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='POS', has_record='Yes', other_record='No')
        HivTestReviewFactory(subject_visit=self.subject_visit_male, recorded_hiv_result='NEG', hiv_test_date=result_date)
        subject_status_helper = SubjectStatusHelper(self.subject_visit_male)
        self.assertIsNone(subject_status_helper.hiv_result)

    def tests_hiv_result4(self):
        """"""
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='POS', has_record='No', other_record='No')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='No', arv_evidence='Yes')
        subject_status_helper = SubjectStatusHelper(self.subject_visit_male)
        self.assertEquals(subject_status_helper.hiv_result, 'POS')

    def tests_hiv_result6(self):
        """Other record confirms a verbal positive as evidence of HIV infection not on ART."""
        self.assertTrue(RequisitionMetaData.objects.filter(appointment=self.subject_visit_male.appointment, lab_entry__requisition_panel__name='Microtube', entry_status=REQUIRED).count() == 1)
        self.assertTrue(RequisitionMetaData.objects.filter(appointment=self.subject_visit_male.appointment, lab_entry__requisition_panel__name='Research Blood Draw', entry_status=NOT_REQUIRED).count() == 1)
        self.assertTrue(RequisitionMetaData.objects.filter(appointment=self.subject_visit_male.appointment, lab_entry__requisition_panel__name='Viral Load', entry_status=NOT_REQUIRED).count() == 1)
        site_rule_groups.autodiscover()
        report_datetime = datetime.today()
        today_date = date.today()
        last_year_date = today_date - timedelta(days=365)
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='POS', has_record='No', other_record='Yes')
        subject_referral_helper = SubjectStatusHelper(self.subject_visit_male)
        self.assertEqual('POS', subject_referral_helper.hiv_result)
        self.assertEqual(False, subject_referral_helper.new_pos)
        self.assertTrue(subject_referral_helper.on_art == None)
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='No', arv_evidence='No')
        subject_referral_helper = SubjectStatusHelper(self.subject_visit_male)
        self.assertEqual('POS', subject_referral_helper.hiv_result)
        self.assertFalse(subject_referral_helper.new_pos)
        self.assertTrue(subject_referral_helper.on_art == False)
        hiv_result_documentation = HivResultDocumentationFactory(subject_visit=self.subject_visit_male, result_recorded='POS', result_date=last_year_date, result_doc_type='ART Prescription')
        subject_referral_helper = SubjectStatusHelper(self.subject_visit_male)
        self.assertEqual('POS', subject_referral_helper.hiv_result)
        self.assertFalse(subject_referral_helper.new_pos)
        self.assertTrue(subject_referral_helper.on_art == False)
        self.assertEqual(hiv_result_documentation.result_date, subject_referral_helper.hiv_result_datetime.date())
        self.assertTrue(ScheduledEntryMetaData.objects.filter(appointment=self.subject_visit_male.appointment, entry__model_name='hivresult', entry_status=NOT_REQUIRED).count() == 1)
        self.assertTrue(ScheduledEntryMetaData.objects.filter(appointment=self.subject_visit_male.appointment, entry__model_name='pima', entry_status=REQUIRED).count() == 1)
        self.assertTrue(RequisitionMetaData.objects.filter(appointment=self.subject_visit_male.appointment, lab_entry__requisition_panel__name='Microtube', entry_status=NOT_REQUIRED).count() == 1)
        self.assertTrue(RequisitionMetaData.objects.filter(appointment=self.subject_visit_male.appointment, lab_entry__requisition_panel__name='Research Blood Draw', entry_status=REQUIRED).count() == 1)
        self.assertTrue(RequisitionMetaData.objects.filter(appointment=self.subject_visit_male.appointment, lab_entry__requisition_panel__name='Viral Load', entry_status=REQUIRED).count() == 1)
        site_rule_groups._registry = {}
