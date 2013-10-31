from datetime import datetime

from edc.map.classes import Mapper, site_mappers

from apps.bcpp_subject.tests.factories import SubjectReferralFactory

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
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime,
            hiv_result='IND')
        self.assertIn('HIV', subject_referral.referral_codes)

    def tests_referred_hiv_urgent(self):
        """if IND refer for HIV testing"""
        report_datetime = datetime.today()
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime,
            hiv_result='IND')
        self.assertTrue(subject_referral.urgent_referral)

    def tests_referred_neg_male(self):
        """if NEG and male, refer for SMC"""
        report_datetime = datetime.today()
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime,
            hiv_result='NEG',
            gender='M')
        self.assertIn('SMC', subject_referral.referral_codes)

    def tests_referred_neg_female_pregnant(self):
        """if NEG and female, and pregnant"""
        report_datetime = datetime.today()
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime,
            hiv_result='NEG',
            gender='F',
            pregnant=True)
        self.assertIn('ANC-NEG', subject_referral.referral_codes)

    def tests_referred_pos_female_pregnant(self):
        """if POS and female, and pregnant"""
        report_datetime = datetime.today()
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime,
            hiv_result='POS',
            gender='F',
            pregnant=True,
            on_art=True)
        self.assertIn('ANC-POS', subject_referral.referral_codes)

    def tests_referred_pos_female_pregnant2(self):
        """if POS and female, and pregnant"""
        report_datetime = datetime.today()
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime,
            hiv_result='POS',
            gender='F',
            pregnant=True)
        self.assertIn('ANC-POS', subject_referral.referral_codes)

    def tests_not_referred_neg_female(self):
        """if NEG and female, no referral"""
        report_datetime = datetime.today()
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime,
            hiv_result='NEG',
            gender='F')
        self.assertEquals('', subject_referral.referral_codes)

    def tests_referred_cd4(self):
        """if POS but no other data, refer for CD4"""
        report_datetime = datetime.today()
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime,
            hiv_result='POS',
            hiv_result_datetime=datetime.today(),
            on_art=None,
            cd4_result=None)
        self.assertIn('CD4', subject_referral.referral_codes)

    def tests_referred_cd4_urgent(self):
        """if POS but no other data, refer for CD4"""
        report_datetime = datetime.today()
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime,
            hiv_result='POS',
            hiv_result_datetime=datetime.today(),
            on_art=None,
            cd4_result=None)
        self.assertTrue(subject_referral.urgent_referral)

    def tests_referred_ccc1(self):
        """if POS, high CD4 and art unknown, """
        report_datetime = datetime.today()
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime,
            hiv_result='POS',
            hiv_result_datetime=datetime.today(),
            on_art=None,
            cd4_result=350)
        self.assertIn('CCC', subject_referral.referral_codes)

    def tests_referred_ccc2(self):
        """if POS, low CD4 and art unknown, """
        report_datetime = datetime.today()
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime,
            hiv_result='POS',
            hiv_result_datetime=datetime.today(),
            on_art=None,
            cd4_result=349)
        self.assertIn('CCC-LOW', subject_referral.referral_codes)

    def tests_referred_ccc2_urgent(self):
        """if POS, low CD4 and art unknown, urgent referral"""
        report_datetime = datetime.today()
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime,
            hiv_result='POS',
            hiv_result_datetime=datetime.today(),
            on_art=None,
            cd4_result=349)
        self.assertTrue(subject_referral.urgent_referral)

    def tests_referred_ccc3(self):
        """if pos, high CD4 and not on art, """
        report_datetime = datetime.today()
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime,
            hiv_result='POS',
            hiv_result_datetime=datetime.today(),
            on_art=False,
            cd4_result=351)
        self.assertIn('CCC-HIGH', subject_referral.referral_codes)

    def tests_referred_masa1(self):
        """if pos, low CD4 and not on art, """
        report_datetime = datetime.today()
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime,
            hiv_result='POS',
            hiv_result_datetime=datetime.today(),
            on_art=False,
            cd4_result=349)
        self.assertIn('CCC-LOW', subject_referral.referral_codes)

    def tests_referred_masa1_urgent(self):
        """if pos, low CD4 and not on art, should be urgent"""
        report_datetime = datetime.today()
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime,
            hiv_result='POS',
            hiv_result_datetime=datetime.today(),
            on_art=False,
            cd4_result=349)
        self.assertTrue(subject_referral.urgent_referral)

    def tests_referred_masa2(self):
        """if pos, high CD4 and on art, """
        report_datetime = datetime.today()
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime,
            hiv_result='POS',
            hiv_result_datetime=datetime.today(),
            on_art=True,
            cd4_result=351)
        self.assertIn('MASA-HIGH', subject_referral.referral_codes)

    def tests_referred_masa3(self):
        """if pos, low CD4 and on art, """
        report_datetime = datetime.today()
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime,
            hiv_result='POS',
            hiv_result_datetime=datetime.today(),
            on_art=True,
            cd4_result=350)
        self.assertIn('MASA-LOW', subject_referral.referral_codes)


""" If HIV positive on ART
    - record date of next scheduled refill or clinic visit (should be recorded on OPD card)
    - record clinic to be attended

If HIV positive not on ART
- record date of scheduled clinic visit (should be within 1wk if possible and on the next available ART clinic day)
- record date of clinic to be attended

If HIV negative
- record date for scheduled counseling regarding SMC
- record location of referral for SMC counseling"""
