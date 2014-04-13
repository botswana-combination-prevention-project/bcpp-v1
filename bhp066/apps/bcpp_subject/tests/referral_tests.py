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


class TestPlotMapper(Mapper):
    map_area = 'test_community8'
    map_code = '097'
    regions = []
    sections = []
    landmarks = []
    gps_center_lat = -25.033192
    gps_center_lon = 25.747139
    radius = 5.5
    location_boundary = ()

site_mappers.register(TestPlotMapper)


class ReferralTests(BaseScheduledModelTestCase):

    community = 'test_community8'

    def tests_referred_hiv(self):
        """if IND refer for HIV testing"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='IND')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('HIV-IND', subject_referral.referral_code)

    def tests_referred_smc1(self):
        """if NEG and male and NOT circumcised, refer for SMC"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='NEG')
        CircumcisionFactory(subject_visit=self.subject_visit_male, circumcised='No')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('SMC-NEG', subject_referral.referral_code)

    def tests_referred_smc2(self):
        """if NEG and male and circumcised, do not refer for SMC"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='NEG')
        CircumcisionFactory(subject_visit=self.subject_visit_male, circumcised='Yes')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertNotIn('SMC', subject_referral.referral_code)

    def tests_referred_smc3(self):
        """if new POS and male and circumcised, do not refer for SMC"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        CircumcisionFactory(subject_visit=self.subject_visit_male, circumcised='Yes')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertNotIn('SMC', subject_referral.referral_code)

    def tests_referred_smc3a(self):
        """if new POS and male and  NOT circumcised, do not refer for SMC"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        CircumcisionFactory(subject_visit=self.subject_visit_male, circumcised='No')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertNotIn('SMC', subject_referral.referral_code)

    def tests_referred_smc4(self):
        """if UNKNOWN HIV status and male and NOT circumcised, refer for SMC"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        #HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='NEG')
        CircumcisionFactory(subject_visit=self.subject_visit_male, circumcised='No')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertEqual('SMC-UNK', subject_referral.referral_code)

    def tests_referred_smc5(self):
        """if UNKNOWN HIV status and male and unknown circ status, refer for SMC"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        #HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='NEG')
        #CircumcisionFactory(subject_visit=self.subject_visit_male, circumcised='Yes')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertEqual('SMC?UNK', subject_referral.referral_code)

    def tests_referred_smc5a(self):
        """if UNKNOWN HIV status and male and unknown circ status, refer for SMC"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        #HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='NEG')
        CircumcisionFactory(subject_visit=self.subject_visit_male, circumcised='Unsure')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertEqual('SMC?UNK', subject_referral.referral_code)

    def tests_referred_smc5b(self):
        """if UNKNOWN HIV status and male and unknown circ status, refer for SMC"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='Declined')
        CircumcisionFactory(subject_visit=self.subject_visit_male, circumcised='Unsure')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertEqual('SMC?UNK', subject_referral.referral_code)

    def tests_referred_smc6(self):
        """if NEG and male and unknown circumcision status, refer for SMC"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='NEG')
        #CircumcisionFactory(subject_visit=self.subject_visit_male, circumcised='Yes')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertEqual('SMC?NEG', subject_referral.referral_code)

    def tests_referred_neg_female_pregnant1(self):
        """if NEG and female, and not pregnant, do not refer"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_female, hiv_result='NEG')
        ReproductiveHealthFactory(subject_visit=self.subject_visit_female, currently_pregnant='No')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertEqual('', subject_referral.referral_code)

    def tests_referred_neg_female_pregnant2(self):
        """if NEG and female, and not pregnant, do not refer"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='NEG', has_record='No', other_record='No')
        HivResultFactory(subject_visit=self.subject_visit_female, hiv_result='Declined')
        ReproductiveHealthFactory(subject_visit=self.subject_visit_female, currently_pregnant='Yes')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertEqual('UNK?-PR', subject_referral.referral_code)

    def tests_referred_pos_female_pregnant(self):
        """if POS and female, pregnant, on-arv, refer ANC-POS"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestReviewFactory(subject_visit=self.subject_visit_female, recorded_hiv_result='POS')
        ReproductiveHealthFactory(subject_visit=self.subject_visit_female, currently_pregnant='Yes')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_female, on_arv='Yes')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertIn('POS#-AN', subject_referral.referral_code)

    def tests_referred_pos_female_pregnant2(self):
        """if newly POS and female, and pregnant, refer"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_female, hiv_result='POS')
        ReproductiveHealthFactory(subject_visit=self.subject_visit_female, currently_pregnant='Yes')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_female, on_arv='No')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertIn('POS!-PR', subject_referral.referral_code)

    def tests_referred_masa_monitoring1(self):
        """if known POS, on ART,  Cd4 lo, refer as MASA monitoring low"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestReviewFactory(subject_visit=self.subject_visit_female, recorded_hiv_result='POS')
        ReproductiveHealthFactory(subject_visit=self.subject_visit_female, currently_pregnant='Yes')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_female, on_arv='No')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertIn('POS#-PR', subject_referral.referral_code)

    def tests_referred_masa_monitoring2(self):
        """if known POS, on ART,  Cd4 hi, refer as MASA monitoring hi"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestReviewFactory(subject_visit=self.subject_visit_female, recorded_hiv_result='POS')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_female, on_arv='Yes')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertIn('MASA-CC', subject_referral.referral_code)

    def tests_referred_pos_female_pregnant3(self):
        """if POS and female, and pregnant, refer ANC-POS"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_female, hiv_result='POS')
        ReproductiveHealthFactory(subject_visit=self.subject_visit_female, currently_pregnant='Yes')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertIn('POS!-PR', subject_referral.referral_code)

    def tests_referred_neg_female(self):
        """if NEG and female, refer ANC-NEG"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_female, hiv_result='NEG')
        ReproductiveHealthFactory(subject_visit=self.subject_visit_female, currently_pregnant='Yes')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertEquals('NEG!-PR', subject_referral.referral_code)

    def tests_referred_cd4(self):
        """if POS but no other data, refer for CD4"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('TST-CD4', subject_referral.referral_code)

    def tests_referred1(self):
        """if known POS, high PIMA CD4 and art unknown, """
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestReviewFactory(subject_visit=self.subject_visit_female, recorded_hiv_result='POS', hiv_test_date=date.today())
        PimaFactory(subject_visit=self.subject_visit_female, cd4_value=351, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertIn('POS#-HI', subject_referral.referral_code)

    def tests_referred2(self):
        """if known POS, low PIMA CD4 and art unknown, """
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestReviewFactory(subject_visit=self.subject_visit_female, recorded_hiv_result='POS')
        PimaFactory(subject_visit=self.subject_visit_female, cd4_value=349, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertIn('POS#-LO', subject_referral.referral_code)

    def tests_referred3(self):
        """if known NEG but not tested today, high PIMA CD4 and art unknown, female"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestReviewFactory(subject_visit=self.subject_visit_female, recorded_hiv_result='NEG')
        PimaFactory(subject_visit=self.subject_visit_female, cd4_value=351, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertEqual('TST-HIV', subject_referral.referral_code)

    def tests_referred4(self):
        """if new POS, high PIMA CD4 and art unknown, """
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS', hiv_result_datetime=datetime.today())
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=351, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('POS!-HI', subject_referral.referral_code)

    def tests_referred5(self):
        """if new POS, low PIMA CD4 and art unknown, """
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS', hiv_result_datetime=datetime.today())
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=349, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('POS!-LO', subject_referral.referral_code)

    def tests_referred_urgent1(self):
        """if existing POS, low PIMA CD4 and art unknown, urgent referral"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestReviewFactory(subject_visit=self.subject_visit_male, recorded_hiv_result='POS')
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=349, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        subject_referral_helper = SubjectReferralHelper(subject_referral)
        self.assertTrue(subject_referral_helper.urgent_referral)

    def tests_referred_urgent2(self):
        """if existing POS, low PIMA CD4 and art no, urgent referral"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestReviewFactory(subject_visit=self.subject_visit_male, recorded_hiv_result='POS')
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=349, report_datetime=datetime.today())
        HivCareAdherenceFactory(subject_visit=self.subject_visit_female, on_arv='No')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        subject_referral_helper = SubjectReferralHelper(subject_referral)
        self.assertTrue(subject_referral_helper.urgent_referral)

    def tests_referred_urgent3(self):
        """if new POS, low PIMA CD4 and art unknown, urgent referral"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS', hiv_result_datetime=datetime.today())
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=349, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        subject_referral_helper = SubjectReferralHelper(subject_referral)
        self.assertTrue(subject_referral_helper.urgent_referral)

    def tests_referred_ccc3(self):
        """if new pos, high PIMA CD4 and not on art, """
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='No')
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=351, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('POS!-HI', subject_referral.referral_code)

    def tests_referred_masa1(self):
        """if new pos, low PIMA CD4 and not on art, """
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='No')
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=349, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('POS!-LO', subject_referral.referral_code)

    def tests_referred_verbal1(self):
        """"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='POS', has_record='No', other_record='No')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='No')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('SMC?UNK', subject_referral.referral_code)

    def tests_hiv_result1(self):
        """"""
        report_datetime = datetime.today()
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='POS', has_record='No', other_record='No')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='Yes', arv_evidence='No')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIsNone(subject_referral.hiv_result)

    def tests_hiv_result2(self):
        """"""
        report_datetime = datetime.today()
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='POS', has_record='Yes', other_record='No')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='Yes', arv_evidence='No')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertEqual(None, subject_referral.hiv_result)
        self.assertEqual(None, subject_referral.hiv_result_datetime)

    def tests_hiv_result2a(self):
        """"""
        report_datetime = datetime.today()
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='POS', has_record='Yes', other_record='No')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='Yes', arv_evidence='No')
        hiv_test_review = HivTestReviewFactory(subject_visit=self.subject_visit_male, recorded_hiv_result='POS')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertEqual('POS', subject_referral.hiv_result)
        self.assertEqual(hiv_test_review.hiv_test_date, subject_referral.hiv_result_datetime.date())

    def tests_hiv_result3(self):
        """"""
        report_datetime = datetime.today()
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='POS', has_record='No', other_record='No')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='No', arv_evidence='Yes')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertEqual('POS', subject_referral.hiv_result)
        self.assertIsNone(subject_referral.hiv_result_datetime)

    def tests_hiv_result3a(self):
        """Evidence of being on ARV as reported on Care and Adherence does NOT confirm a verbal positive as evidence of HIV infection"""
        report_datetime = datetime.today()
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='POS', has_record='No', other_record='No')
        hiv_care_adherence = HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='No', arv_evidence='Yes')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertEqual('POS', subject_referral.hiv_result)
        self.assertEqual(hiv_care_adherence.first_arv, subject_referral.hiv_result_datetime.date())

    def tests_hiv_result4(self):
        """Other record confirms a verbal positive as evidence of HIV infection."""
        report_datetime = datetime.today()
        today_date = date.today()
        last_year_date = today_date - timedelta(days=365)
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='POS', has_record='No', other_record='Yes')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='No', arv_evidence='No')
        hiv_result_documentation = HivResultDocumentationFactory(subject_visit=self.subject_visit_male, result_recorded='POS', result_date=last_year_date, result_doc_type='ART Prescription')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertEqual('POS', subject_referral.hiv_result)
        self.assertEqual(hiv_result_documentation.result_date, subject_referral.hiv_result_datetime.date())

    def tests_hiv_result4a(self):
        """Other record confirms a verbal positive as evidence of HIV infection not on ART."""
        from ..classes import SubjectStatusHelper

        report_datetime = datetime.today()
        today_date = date.today()
        last_year_date = today_date - timedelta(days=365)
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='POS', has_record='No', other_record='Yes')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='No', arv_evidence='No')
        hiv_result_documentation = HivResultDocumentationFactory(subject_visit=self.subject_visit_male, result_recorded='POS', result_date=last_year_date, result_doc_type='ART Prescription')
        subject_referral = SubjectStatusHelper(self.subject_visit_male)
        self.assertEqual('POS', subject_referral.hiv_result)
        self.assertFalse(subject_referral.new_pos)
        self.assertTrue(subject_referral.on_art == False)
        #self.assertEqual(hiv_result_documentation.result_date, subject_referral.hiv_result_datetime.date())
        self.assertTrue(ScheduledEntryMetaData.objects.filter(appointment=self.subject_visit_male.appointment, entry__model_name='hivresult', entry_status=REQUIRED).count() == 1)
        self.assertTrue(ScheduledEntryMetaData.objects.filter(appointment=self.subject_visit_male.appointment, entry__model_name='pima', entry_status=REQUIRED).count() == 1)

    def tests_referred_verbal1b(self):
        """"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='POS', other_record='Yes')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='No')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('TST-CD4', subject_referral.referral_code)

    def tests_referred_verbal2(self):
        """"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='POS', other_record='Yes')
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='No')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('TST-CD4', subject_referral.referral_code)

    def tests_referred_verbal3(self):
        """"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='POS', other_record='Yes')
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='No')
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=349, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('POS#-LO', subject_referral.referral_code)

    def tests_referred_verbal4(self):
        """"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='POS', other_record='Yes')
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='No')
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=351, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('POS#-HI', subject_referral.referral_code)

    def tests_referred_verbal5(self):
        """"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='POS', other_record='Yes')
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='Yes')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('MASA-CC', subject_referral.referral_code)

    def tests_referred_verbal6(self):
        """"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='POS', other_record='Yes')
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='Yes')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('MASA-CC', subject_referral.referral_code)

    def tests_referred_masa2(self):
        """if new pos, high PIMA CD4 and on art, """
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='Yes')
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=351, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('MASA-CC', subject_referral.referral_code)

    def tests_referred_masa3(self):
        """if pos, low CD4 and on art, """
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='Yes')
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=350, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('MASA-CC', subject_referral.referral_code)

    def tests_referred_masa4(self):
        """Tests pos today but have evidence on ART"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='No', arv_evidence='Yes')
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=350, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('MASA-DF', subject_referral.referral_code)

    def tests_referred_masa5(self):
        """if pos and defaulter """
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestReviewFactory(subject_visit=self.subject_visit_female, recorded_hiv_result='POS')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_female, on_arv='No', arv_evidence='Yes')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertIn('MASA-DF', subject_referral.referral_code)

    def tests_subject_referral_field_attr1(self):
        report_datetime = datetime.today()
        today = datetime.today()
        today_date = datetime.today()
        last_year_date = today_date - timedelta(days=365)
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.site_code, is_drawn='Yes', panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'), drawn_datetime=datetime.today())
        TbSymptomsFactory(subject_visit=self.subject_visit_female)
        HivResultFactory(subject_visit=self.subject_visit_female, hiv_result='POS', hiv_result_datetime=today)
        HivTestReviewFactory(subject_visit=self.subject_visit_female, recorded_hiv_result='POS', hiv_test_date=last_year_date)
        HivCareAdherenceFactory(subject_visit=self.subject_visit_female, on_arv='Yes', arv_evidence='Yes')
        PimaFactory(subject_visit=self.subject_visit_female, cd4_value=350, report_datetime=report_datetime, cd4_datetime=today)
        panel = Panel.objects.get(name='Viral Load')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.site_code, is_drawn='Yes', panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'), drawn_datetime=today)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime,
            referral_clinic='Otse')
        subject_referral_helper = SubjectReferralHelper(subject_referral)
        expected = {
            'arv_documentation': True,
            'arv_clinic': None,
            'cd4_result': 350,
            'cd4_result_datetime': today,
            'circumcised': None,
            'citizen': True,
            'citizen_spouse': False,
            'direct_hiv_documentation': True,
            'gender': u'F',
            'hiv_result': u'POS',
            'hiv_result_datetime': today,
            'indirect_hiv_documentation': None,
            'last_hiv_result': u'POS',
            'new_pos': False,
            'next_arv_clinic_appointment_date': None,
            'on_art': True,
            'permanent_resident': None,
            'pregnant': None,
            'referral_clinic': 'Otse',
            'referral_code': 'MASA-CC',
            'tb_symptoms': 'cough, cough_blood, night_sweat',
            'urgent_referral': False,
            'verbal_hiv_result': None,
            'vl_sample_drawn': True,
            'vl_sample_drawn_datetime': today}
        self.assertDictContainsSubset(expected, subject_referral_helper.subject_referral)

    def tests_subject_referral_field_attr2(self):
        report_datetime = datetime.today()
        today = datetime.today()
        today_date = date.today()
        last_year_date = today_date - timedelta(days=365)
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.site_code, is_drawn='Yes', panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'), drawn_datetime=datetime.today())
        TbSymptomsFactory(subject_visit=self.subject_visit_female)
        # verbal POS with indirect docs
        HivTestingHistoryFactory(subject_visit=self.subject_visit_female, verbal_hiv_result='POS', has_record='No', other_record='Yes')
        #
        HivResultDocumentationFactory(subject_visit=self.subject_visit_female, result_recorded='POS', result_date=last_year_date, result_doc_type='ART Prescription')
        # on ART and there are docs 
        HivCareAdherenceFactory(subject_visit=self.subject_visit_female, on_arv='Yes', arv_evidence='Yes')
        panel = Panel.objects.get(name='Viral Load')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.site_code, is_drawn='Yes', panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'), drawn_datetime=today)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime,
            referral_clinic='Otse')
        subject_referral_helper = SubjectReferralHelper(subject_referral)
        expected = {
            'arv_documentation': True,
            'arv_clinic': None,
            'cd4_result': None,
            'cd4_result_datetime': None,
            'circumcised': None,
            'citizen': True,
            'citizen_spouse': False,
            'direct_hiv_documentation': False,
            'gender': u'F',
            'hiv_result': u'POS',
            'hiv_result_datetime': datetime(last_year_date.year, last_year_date.month, last_year_date.day),
            'indirect_hiv_documentation': True,
            'last_hiv_result': u'POS',
            'new_pos': False,
            'next_arv_clinic_appointment_date': None,
            'on_art': True,
            'permanent_resident': None,
            'pregnant': None,
            'referral_clinic': 'Otse',
            'referral_code': 'MASA-CC',
            'tb_symptoms': 'cough, cough_blood, night_sweat',
            'urgent_referral': False,
            'verbal_hiv_result': 'POS',
            'vl_sample_drawn': True,
            'vl_sample_drawn_datetime': today}
        self.assertDictContainsSubset(expected, subject_referral_helper.subject_referral)

    def tests_subject_referral_field_attr3(self):
        yesterday = datetime.today() - timedelta(days=1)
        report_datetime = datetime.today()
        today = datetime.today()
        today_date = date.today()
        last_year_date = today_date - timedelta(days=365)
        panel = Panel.objects.get(name='Microtube')
        self.subject_visit_female.report_datetime = yesterday
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.site_code, is_drawn='Yes', panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'), drawn_datetime=yesterday)
        # verbal POS with indirect docs
        HivTestingHistoryFactory(subject_visit=self.subject_visit_female, report_datetime=yesterday, verbal_hiv_result='POS', has_record='No', other_record='No')
        # on ART and there are docs
        HivCareAdherenceFactory(subject_visit=self.subject_visit_female, report_datetime=yesterday, ever_taken_arv='Yes', on_arv='No', arv_stop_date=last_year_date, arv_evidence='Yes')

        panel = Panel.objects.get(name='Viral Load')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.site_code, is_drawn='Yes', panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'), drawn_datetime=yesterday)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime,
            referral_clinic='Otse')
        subject_referral_helper = SubjectReferralHelper(subject_referral)
        expected = {
            'arv_documentation': True,
            'arv_clinic': None,
            'cd4_result': None,
            'cd4_result_datetime': None,
            'circumcised': None,
            'citizen': True,
            'citizen_spouse': False,
            'direct_hiv_documentation': False,
            'gender': u'F',
            'hiv_result': 'POS',
            'hiv_result_datetime': None,
            'indirect_hiv_documentation': True,
            'last_hiv_result': None,
            'new_pos': False,
            'next_arv_clinic_appointment_date': None,
            'on_art': True,
            'permanent_resident': None,
            'pregnant': None,
            'referral_clinic': 'Otse',
            'referral_code': 'MASA-DF',
            'tb_symptoms': '',
            'urgent_referral': True,
            'verbal_hiv_result': 'POS',
            'vl_sample_drawn': True,
            'vl_sample_drawn_datetime': yesterday}
        self.assertDictContainsSubset(expected, subject_referral_helper.subject_referral)

    def tests_subject_referral_field_attr4(self):
        yesterday = datetime.today() - timedelta(days=1)
        report_datetime = datetime.today()
        today = datetime.today()
        today_date = date.today()
        last_year_date = today_date - timedelta(days=365)
        panel = Panel.objects.get(name='Microtube')
        self.subject_visit_female.report_datetime = yesterday
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.site_code, is_drawn='Yes', panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'), drawn_datetime=yesterday)
        # verbal POS with indirect docs
        HivTestingHistoryFactory(subject_visit=self.subject_visit_female, report_datetime=yesterday, verbal_hiv_result='POS', has_record='No', other_record='No')
        # on ART and there are docs 
        HivCareAdherenceFactory(subject_visit=self.subject_visit_female, report_datetime=yesterday, ever_taken_arv='Yes', on_arv='No', arv_stop_date=last_year_date, arv_evidence='Yes')
        HivResultFactory(subject_visit=self.subject_visit_female, hiv_result='POS', hiv_result_datetime=yesterday)
        panel = Panel.objects.get(name='Viral Load')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.site_code, is_drawn='Yes', panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'), drawn_datetime=yesterday)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime,
            referral_clinic='Otse')
        subject_referral_helper = SubjectReferralHelper(subject_referral)
        expected = {
            'arv_documentation': True,
            'arv_clinic': None,
            'cd4_result': None,
            'cd4_result_datetime': None,
            'circumcised': None,
            'citizen': True,
            'citizen_spouse': False,
            'direct_hiv_documentation': False,
            'gender': u'F',
            'hiv_result': 'POS',
            'hiv_result_datetime': yesterday,
            'indirect_hiv_documentation': True,
            'last_hiv_result': None,  # undocumented verbal_hiv_result cannot be the last result
            'new_pos': False,  # undocumented verbal_hiv_result can suggest not a new POS
            'next_arv_clinic_appointment_date': None,
            'on_art': True,
            'permanent_resident': None,
            'pregnant': None,
            'referral_clinic': 'Otse',
            'referral_code': 'MASA-DF',
            'tb_symptoms': '',
            'urgent_referral': True,  # because this is a defaulter
            'verbal_hiv_result': 'POS',
            'vl_sample_drawn': True,
            'vl_sample_drawn_datetime': yesterday}
        self.assertDictContainsSubset(expected, subject_referral_helper.subject_referral)

    def tests_subject_referral_field_attr5(self):
        """if IND refer for HIV testing"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='POS', has_record='No', other_record='No')
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='Declined')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        subject_referral_helper = SubjectReferralHelper(subject_referral)
        expected = {
            'direct_hiv_documentation': False,
            'indirect_hiv_documentation': False,
            'last_hiv_result': None,  # undocumented verbal_hiv_result cannot be the last result
            'last_hiv_result_date': None,  # undocumented verbal_hiv_result cannot be the last result
            'new_pos': None,  # undocumented verbal_hiv_result can suggest not a new POS
            'verbal_hiv_result': 'POS',
            'hiv_result': None}
        self.assertDictContainsSubset(expected, subject_referral_helper.subject_referral)

    def tests_subject_referral_field_attr6(self):
        """if IND refer for HIV testing"""
        report_datetime = datetime.today()
        last_date = report_datetime.date() - relativedelta(years=3)
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='POS', has_record='Yes', other_record='No')
        HivTestReviewFactory(subject_visit=self.subject_visit_male, hiv_test_date=last_date, recorded_hiv_result='NEG')
        #HivResultDocumentationFactory(subject_visit=self.subject_visit_male, result_date=report_datetime - relativedelta(years=1), result_recorded='POS', result_doc_type='Record of CD4 count')
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='Declined')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        subject_referral_helper = SubjectReferralHelper(subject_referral)
        expected = {
            'direct_hiv_documentation': False,  # of positive result
            'indirect_hiv_documentation': False,
            'last_hiv_result': 'NEG',
            'last_hiv_result_date': last_date,
            'new_pos': None,
            'verbal_hiv_result': 'POS',
            'hiv_result': None}
        self.assertDictContainsSubset(expected, subject_referral_helper.subject_referral)

    def tests_subject_referral_field_attr7(self):
        """ """
        report_datetime = datetime.today()
        last_date = report_datetime.date() - relativedelta(years=3)
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='POS', has_record='Yes', other_record='Yes')
        HivTestReviewFactory(subject_visit=self.subject_visit_male, hiv_test_date=last_date, recorded_hiv_result='NEG')
        HivResultDocumentationFactory(subject_visit=self.subject_visit_male, result_date=report_datetime - relativedelta(years=1), result_recorded='POS', result_doc_type='Record of CD4 count')
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='Declined')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        subject_referral_helper = SubjectReferralHelper(subject_referral)
        expected = {
            'direct_hiv_documentation': False,
            'indirect_hiv_documentation': True,
            'last_hiv_result': 'NEG',
            'last_hiv_result_date': last_date,
            'new_pos': False,
            'verbal_hiv_result': 'POS',
            'hiv_result': 'POS'}
        self.assertDictContainsSubset(expected, subject_referral_helper.subject_referral)

    def tests_subject_referral_field_attr8(self):
        """ """
        report_datetime = datetime.today()
        last_date = report_datetime.date() - relativedelta(years=3)
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='POS', has_record='Yes', other_record='Yes')
        HivTestReviewFactory(subject_visit=self.subject_visit_male, hiv_test_date=last_date, recorded_hiv_result='POS')
        HivResultDocumentationFactory(subject_visit=self.subject_visit_male, result_date=report_datetime - relativedelta(years=1), result_recorded='POS', result_doc_type='Record of CD4 count')
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='Declined')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        subject_referral_helper = SubjectReferralHelper(subject_referral)
        expected = {
            'direct_hiv_documentation': True,
            'indirect_hiv_documentation': True,
            'last_hiv_result': 'POS',
            'last_hiv_result_date': last_date,
            'new_pos': False,
            'verbal_hiv_result': 'POS',
            'hiv_result': 'POS'}
        self.assertDictContainsSubset(expected, subject_referral_helper.subject_referral)

    def tests_subject_referral_field_attr9(self):
        """ """
        report_datetime = datetime.today()
        #last_date = report_datetime.date() - relativedelta(years=3)
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.site_code, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='POS', has_record='Yes', other_record='Yes')
        #HivTestReviewFactory(subject_visit=self.subject_visit_male, hiv_test_date=last_date, recorded_hiv_result='POS')
        #HivResultDocumentationFactory(subject_visit=self.subject_visit_male, result_date=report_datetime - relativedelta(years=1), result_recorded='POS', result_doc_type='Record of CD4 count')
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        subject_referral_helper = SubjectReferralHelper(subject_referral)
        expected = {
            'direct_hiv_documentation': False,
            'indirect_hiv_documentation': True,
            'last_hiv_result': None,
            'last_hiv_result_date': None,
            'new_pos': False,
            'verbal_hiv_result': 'POS',
            'hiv_result': 'POS'}
        self.assertDictContainsSubset(expected, subject_referral_helper.subject_referral)
