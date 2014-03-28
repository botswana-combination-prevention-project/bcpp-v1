from datetime import datetime

from edc.map.classes import Mapper, site_mappers

from apps.bcpp_lab.models import AliquotType, Panel
from apps.bcpp_lab.tests.factories import SubjectRequisitionFactory
from .base_scheduled_model_test_case import BaseScheduledModelTestCase
from .factories import (SubjectReferralFactory, ReproductiveHealthFactory,
                                               HivCareAdherenceFactory, HivResultFactory, CircumcisionFactory,
                                               PimaFactory, HivTestReviewFactory,
                                               Cd4HistoryFactory)


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
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='IND')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('HIV-IND', subject_referral.referral_code)

    def tests_referred_smc1(self):
        """if NEG and male and NOT circumcised, refer for SMC"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='NEG')
        CircumcisionFactory(subject_visit=self.subject_visit_male, circumcised='No')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('SMC-NEG', subject_referral.referral_code)

    def tests_referred_smc2(self):
        """if NEG and male and NOT circumcised, do not refer for SMC"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='NEG')
        CircumcisionFactory(subject_visit=self.subject_visit_male, circumcised='Yes')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertNotIn('SMC-NEG', subject_referral.referral_code)

    def tests_referred_smc3(self):
        """if new POS and male and NOT circumcised, do not refer for SMC"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        CircumcisionFactory(subject_visit=self.subject_visit_male, circumcised='Yes')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertNotIn('SMC', subject_referral.referral_code)

    def tests_referred_neg_female_pregnant(self):
        """if NEG and female, and not pregnant, do not refer"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_female, hiv_result='NEG')
        ReproductiveHealthFactory(subject_visit=self.subject_visit_female, currently_pregnant='No')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertEqual('', subject_referral.referral_code)

    def tests_referred_pos_female_pregnant(self):
        """if POS and female, pregnant, on-arv, refer ANC-POS"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
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
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
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
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestReviewFactory(subject_visit=self.subject_visit_female, recorded_hiv_result='POS')
        Cd4HistoryFactory(subject_visit=self.subject_visit_female, last_cd4_count=349)
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
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestReviewFactory(subject_visit=self.subject_visit_female, recorded_hiv_result='POS')
        Cd4HistoryFactory(subject_visit=self.subject_visit_female, last_cd4_count=351)
        HivCareAdherenceFactory(subject_visit=self.subject_visit_female, on_arv='No')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertIn('TST-CD4', subject_referral.referral_code)

    def tests_referred_pos_female_pregnant3(self):
        """if POS and female, and pregnant, refer ANC-POS"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
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
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
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
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('TST-CD4', subject_referral.referral_code)

    def tests_referred1(self):
        """if known POS, high PIMA CD4 and art unknown, """
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestReviewFactory(subject_visit=self.subject_visit_female, recorded_hiv_result='POS')
        PimaFactory(subject_visit=self.subject_visit_female, cd4_value=351, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertIn('POS#-HI', subject_referral.referral_code)

    def tests_referred2(self):
        """if known POS, low PIMA CD4 and art unknown, """
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestReviewFactory(subject_visit=self.subject_visit_female, recorded_hiv_result='POS')
        PimaFactory(subject_visit=self.subject_visit_female, cd4_value=349, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertIn('POS#-LO', subject_referral.referral_code)

    def tests_referred3(self):
        """if known NEG, high PIMA CD4 and art unknown, female"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestReviewFactory(subject_visit=self.subject_visit_female, recorded_hiv_result='NEG')
        PimaFactory(subject_visit=self.subject_visit_female, cd4_value=351, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertEqual('', subject_referral.referral_code)

    def tests_referred4(self):
        """if new POS, high PIMA CD4 and art unknown, """
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
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
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
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
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestReviewFactory(subject_visit=self.subject_visit_male, recorded_hiv_result='POS')
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=349, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertTrue(subject_referral.urgent_referral)

    def tests_referred_urgent2(self):
        """if existing POS, low PIMA CD4 and art no, urgent referral"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestReviewFactory(subject_visit=self.subject_visit_male, recorded_hiv_result='POS')
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=349, report_datetime=datetime.today())
        HivCareAdherenceFactory(subject_visit=self.subject_visit_female, on_arv='No')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertTrue(subject_referral.urgent_referral)

    def tests_referred_urgent3(self):
        """if new POS, low PIMA CD4 and art unknown, urgent referral"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS', hiv_result_datetime=datetime.today())
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=349, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertTrue(subject_referral.urgent_referral)

    def tests_referred_ccc3(self):
        """if new pos, high PIMA CD4 and not on art, """
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
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
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='No')
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=349, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('ERROR', subject_referral.referral_code)

    def tests_referred_masa2(self):
        """if new pos, high PIMA CD4 and on art, """
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='Yes')
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=351, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('ERROR', subject_referral.referral_code)

    def tests_referred_masa3(self):
        """if pos, low CD4 and on art, """
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='Yes')
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=350, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('ERROR', subject_referral.referral_code)

    def tests_referred_masa4(self):
        """should not be asking for arv info on unknown status """
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='No', arv_evidence='Yes')
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=350, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('ERROR', subject_referral.referral_code)

    def tests_referred_masa5(self):
        """if pos and defaulter """
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestReviewFactory(subject_visit=self.subject_visit_female, recorded_hiv_result='POS')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_female, on_arv='No', arv_evidence='Yes')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertIn('MASA-DF', subject_referral.referral_code)
