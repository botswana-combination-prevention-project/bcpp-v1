from datetime import datetime

from edc.map.classes import Mapper, site_mappers

from apps.bcpp_subject.tests.factories import SubjectReferralFactory, ReproductiveHealthFactory, HivCareAdherenceFactory, HivResultFactory, CircumcisionFactory, PimaFactory

from .base_scheduled_model_test_case import BaseScheduledModelTestCase


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
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='IND')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('HIV', subject_referral.referral_codes)

    def tests_referred_hiv_urgent(self):
        """if IND refer for HIV testing"""
        report_datetime = datetime.today()
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='IND')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertTrue(subject_referral.urgent_referral)

    def tests_referred_neg_male(self):
        """if NEG and male, refer for SMC"""
        report_datetime = datetime.today()
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='NEG')
        CircumcisionFactory(subject_visit=self.subject_visit_male, circumcised='No')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('SMC', subject_referral.referral_codes)

    def tests_referred_neg_female_pregnant(self):
        """if NEG and female, and pregnant"""
        report_datetime = datetime.today()
        HivResultFactory(subject_visit=self.subject_visit_female, hiv_result='NEG')
        ReproductiveHealthFactory(subject_visit=self.subject_visit_female, currently_pregnant='No')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertIn('NOT_REFERRED', subject_referral.referral_codes)

    def tests_referred_pos_female_pregnant(self):
        """if POS and female, and pregnant"""
        report_datetime = datetime.today()
        HivResultFactory(subject_visit=self.subject_visit_female, hiv_result='POS')
        ReproductiveHealthFactory(subject_visit=self.subject_visit_female, currently_pregnant='Yes')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='Yes')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertIn('ANC-POS', subject_referral.referral_codes)

    def tests_referred_pos_female_pregnant2(self):
        """if POS and female, and pregnant"""
        report_datetime = datetime.today()
        HivResultFactory(subject_visit=self.subject_visit_female, hiv_result='POS')
        ReproductiveHealthFactory(subject_visit=self.subject_visit_female, currently_pregnant='Yes')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertIn('ANC-POS', subject_referral.referral_codes)

    def tests_referred_neg_female(self):
        """if NEG and female, no referral"""
        report_datetime = datetime.today()
        HivResultFactory(subject_visit=self.subject_visit_female, hiv_result='NEG')
        ReproductiveHealthFactory(subject_visit=self.subject_visit_female, currently_pregnant='Yes')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertEquals('ANC-NEG', subject_referral.referral_codes)

    def tests_referred_pos_female_pregnant3(self):
        """if POS and female, and pregnant"""
        report_datetime = datetime.today()
        HivResultFactory(subject_visit=self.subject_visit_female, hiv_result='POS')
        ReproductiveHealthFactory(subject_visit=self.subject_visit_female, currently_pregnant='Yes')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertIn('ANC-POS', subject_referral.referral_codes)

    def tests_referred_cd4(self):
        """if POS but no other data, refer for CD4"""
        report_datetime = datetime.today()
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('CD4', subject_referral.referral_codes)

    def tests_referred_cd4_urgent(self):
        """if POS but no other data, refer for CD4"""
        report_datetime = datetime.today()
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertTrue(subject_referral.urgent_referral)

    def tests_referred_ccc1(self):
        """if POS, high CD4 and art unknown, """
        report_datetime = datetime.today()
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS', hiv_result_datetime=datetime.today())
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=350, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('CCC', subject_referral.referral_codes)

    def tests_referred_ccc2(self):
        """if POS, low CD4 and art unknown, """
        report_datetime = datetime.today()
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=349, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('CCC-LOW', subject_referral.referral_codes)

    def tests_referred_ccc2_urgent(self):
        """if POS, low CD4 and art unknown, urgent referral"""
        report_datetime = datetime.today()
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=349, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertTrue(subject_referral.urgent_referral)

    def tests_referred_ccc3(self):
        """if pos, high CD4 and not on art, """
        report_datetime = datetime.today()
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='No')
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=351, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('CCC-HIGH', subject_referral.referral_codes)

    def tests_referred_masa1(self):
        """if pos, low CD4 and not on art, """
        report_datetime = datetime.today()
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='No')
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=349, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('CCC-LOW', subject_referral.referral_codes)

    def tests_referred_masa1_urgent(self):
        """if pos, low CD4 and not on art, should be urgent"""
        report_datetime = datetime.today()
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='No')
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=349, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertTrue(subject_referral.urgent_referral)

    def tests_referred_masa2(self):
        """if pos, high CD4 and on art, """
        report_datetime = datetime.today()
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='Yes')
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=351, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('MASA-HIGH', subject_referral.referral_codes)

    def tests_referred_masa3(self):
        """if pos, low CD4 and on art, """
        report_datetime = datetime.today()
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='Yes')
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=350, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('MASA-LOW', subject_referral.referral_codes)

    def tests_referred_masa4(self):
        """if pos and defaulter """
        report_datetime = datetime.today()
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='No', arv_evidence='Yes')
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=350, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('MASA-DEFAULTER', subject_referral.referral_codes)

""" If HIV positive on ART
    - record date of next scheduled refill or clinic visit (should be recorded on OPD card)
    - record clinic to be attended

If HIV positive not on ART
- record date of scheduled clinic visit (should be within 1wk if possible and on the next available ART clinic day)
- record date of clinic to be attended

If HIV negative
- record date for scheduled counseling regarding SMC
- record location of referral for SMC counseling"""
