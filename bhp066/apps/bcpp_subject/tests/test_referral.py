from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from django.core.management import call_command

from edc.map.classes import Mapper, site_mappers
from edc.notification.models import Notification, NotificationPlan
from edc.export.models import ExportPlan

from apps.bcpp_lab.models import AliquotType, Panel
from apps.bcpp_lab.tests.factories import SubjectRequisitionFactory

from ..classes import SubjectReferralHelper

from .base_scheduled_model_test_case import BaseScheduledModelTestCase
from .factories import (
    SubjectReferralFactory, ReproductiveHealthFactory,
    HivCareAdherenceFactory, HivResultFactory, CircumcisionFactory,
    PimaFactory, HivTestReviewFactory, HivTestingHistoryFactory, TbSymptomsFactory,
    HivResultDocumentationFactory)
from edc.subject.appointment.models import Appointment
from edc.entry_meta_data.models.scheduled_entry_meta_data import ScheduledEntryMetaData
from edc.constants import NOT_REQUIRED, REQUIRED, NOT_APPLICABLE
from edc.entry_meta_data.models.requisition_meta_data import RequisitionMetaData
from edc.export.models.export_transaction import ExportTransaction
from apps.bcpp_subject.tests.factories.subject_locator_factory import SubjectLocatorFactory
from apps.bcpp_household_member.tests.factories import HouseholdMemberFactory, EnrollmentChecklistFactory
from apps.bcpp_household.constants import BASELINE_SURVEY_SLUG
from apps.bcpp_subject.tests.factories import SubjectConsentFactory, SubjectVisitFactory
from apps.bcpp_subject.models import HivCareAdherence, HivTestingHistory, HivTestReview


# class TestPlotMapper(Mapper):
#     map_area = 'mmankgodi'
#     map_code = '19'  # has to be a code in the clinic days dictionary
#     regions = []
#     sections = []
#     landmarks = []
#     gps_center_lat = -25.033192
#     gps_center_lon = 25.747139
#     radius = 5.5
#     location_boundary = ()
#  
# site_mappers.register(TestPlotMapper)


class TestReferral(BaseScheduledModelTestCase):

    community = 'lerala'
    site_code = '21'

    def startup(self):
        super(TestReferral, self).startup()
        SubjectLocatorFactory(subject_visit=self.subject_visit_male)
        SubjectLocatorFactory(subject_visit=self.subject_visit_female)

    def tests_referred_hiv(self):
        """if IND refer for HIV testing"""
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='IND')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('', subject_referral.referral_code)

    def referral_smc1(self):
        self.startup()
        report_datetime = self.subject_visit_male.report_datetime
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='NEG')
        CircumcisionFactory(subject_visit=self.subject_visit_male, circumcised='No')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('SMC-NEG', subject_referral.referral_code)

        report_datetime = self.subject_visit_male_annual.report_datetime
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(
            subject_visit=self.subject_visit_male_annual,
            site=self.study_site, panel=panel,
            aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male_annual, hiv_result='NEG')
        CircumcisionFactory(subject_visit=self.subject_visit_male_annual, circumcised='No')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male_annual,
            report_datetime=report_datetime)
        return subject_referral

    def tests_referred_smc1(self):
        """if NEG and male and NOT circumcised, refer for SMC in Y1 intervention
        and also refer in Y2 intervention"""
        site_mappers.current_mapper.intervention = True
        subject_referral = self.referral_smc1()
        self.assertIn('SMC-NEG', subject_referral.referral_code)

    def tests_referred_smc1a(self):
        """if NEG and male and NOT circumcised, refer for SMC in Y1 non-intervention
        and do not refer in Y2 non-intervention"""
        site_mappers.current_mapper.intervention = False
        subject_referral = self.referral_smc1()
        self.assertEqual('', subject_referral.referral_code)

    def referral_smc2(self):
        self.startup()
        report_datetime = self.subject_visit_male.report_datetime
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='NEG')
        CircumcisionFactory(subject_visit=self.subject_visit_male, circumcised='Yes')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertNotIn('SMC', subject_referral.referral_code)

        report_datetime = self.subject_visit_male_annual.report_datetime
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male_annual,
            report_datetime=report_datetime)
        return subject_referral

    def tests_referred_smc2(self):
        """if NEG and male and circumcised, do not refer for SMC, both Y1 and Y2 intervention"""
        site_mappers.current_mapper.intervention = True
        subject_referral = self.referral_smc2()
        self.assertNotIn('SMC', subject_referral.referral_code)

    def tests_referred_smc2a(self):
        """if NEG and male and circumcised, do not refer for SMC, both Y1 and Y2 non-intervention"""
        site_mappers.current_mapper.intervention = False
        subject_referral = self.referral_smc2()
        self.assertNotIn('SMC', subject_referral.referral_code)

    def tests_circumsised_y2_not_smc(self):
        """if NEG and male and not circumcised in Y1, then refer for SMC in Y1. 
            Then if male circumsised in Y2 then do not refer for SMC in Y2."""
        self.startup()
        report_datetime = self.subject_visit_male.report_datetime
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='NEG')
        CircumcisionFactory(subject_visit=self.subject_visit_male, circumcised='No')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('SMC', subject_referral.referral_code)

        report_datetime = self.subject_visit_male_annual.report_datetime
        CircumcisionFactory(subject_visit=self.subject_visit_male_annual, circumcised='Yes')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male_annual,
            report_datetime=report_datetime)
        self.assertNotIn('SMC', subject_referral.referral_code)

    def tests_referred_smc3(self):
        """if new POS and male and circumcised, do not refer for SMC"""
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        CircumcisionFactory(subject_visit=self.subject_visit_male, circumcised='Yes')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertNotIn('SMC', subject_referral.referral_code)

    def tests_export_referred_smc3(self):
        """if new POS and male and circumcised, do not refer for SMC"""
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        CircumcisionFactory(subject_visit=self.subject_visit_male, circumcised='Yes')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertNotIn('SMC', subject_referral.referral_code)
        self.assertEqual(2, NotificationPlan.objects.all().count())
        self.assertEqual(2, ExportPlan.objects.all().count())
        export_plan = ExportPlan.objects.get(object_name='SubjectReferral')
        export_plan.target_path = '~/'
        export_plan.save()
        self.assertEqual(0, Notification.objects.all().count())
        call_command('export_transactions bcpp_subject.subjectreferral')
        self.assertEqual(1, Notification.objects.all().count())

    def tests_referred_smc3a(self):
        """if new POS and male and  NOT circumcised, do not refer for SMC"""
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        CircumcisionFactory(subject_visit=self.subject_visit_male, circumcised='No')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertNotIn('SMC', subject_referral.referral_code)

    def tests_referred_smc4(self):
        """if UNKNOWN HIV status and male and NOT circumcised, refer for SMC"""
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        #HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='NEG')
        CircumcisionFactory(subject_visit=self.subject_visit_male, circumcised='No')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertEqual('SMC-UNK', subject_referral.referral_code)

    def referral_smc5(self):
        self.startup()
        report_datetime = self.subject_visit_male.report_datetime
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(
            subject_visit=self.subject_visit_male,
            site=self.study_site,
            panel=panel,
            aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertEqual('SMC?UNK', subject_referral.referral_code)

        report_datetime = self.subject_visit_male_annual.report_datetime
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(
            subject_visit=self.subject_visit_male_annual,
            site=self.study_site,
            panel=panel,
            aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male_annual,
            report_datetime=report_datetime)
        return subject_referral

    def tests_referred_smc5(self):
        """if UNKNOWN HIV status and male and unknown circ status, refer for SMC"""
        site_mappers.current_mapper.intervention = True
        subject_referral = self.referral_smc5()
        self.assertEqual('SMC?UNK', subject_referral.referral_code)

    def tests_referred_smc5a(self):
        """if UNKNOWN HIV status and male and unknown circ status, refer for SMC"""
        site_mappers.current_mapper.intervention = False
        subject_referral = self.referral_smc5()
        self.assertEqual('', subject_referral.referral_code)

    def tests_referred_smc6(self):
        """if UNKNOWN HIV status and male and unknown circ status, refer for SMC"""
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        # HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='NEG')
        CircumcisionFactory(subject_visit=self.subject_visit_male, circumcised='Unsure')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertEqual('SMC?UNK', subject_referral.referral_code)

    def tests_referred_smc5b(self):
        """if UNKNOWN HIV status and male and unknown circ status, refer for SMC"""
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='Declined')
        CircumcisionFactory(subject_visit=self.subject_visit_male, circumcised='Unsure')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertEqual('SMC?UNK', subject_referral.referral_code)

    def tests_referred_smc7(self):
        """if NEG and male and unknown circumcision status, refer for SMC"""
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='NEG')
        #CircumcisionFactory(subject_visit=self.subject_visit_male, circumcised='Yes')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertEqual('SMC?NEG', subject_referral.referral_code)

    def tests_referred_neg_female_pregnant1(self):
        """if NEG and female, and not pregnant, do not refer"""
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_female, hiv_result='NEG')
        ReproductiveHealthFactory(subject_visit=self.subject_visit_female, currently_pregnant='No')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertEqual('', subject_referral.referral_code)

    def tests_referred_neg_female_pregnant2(self):
        """if NEG and female, and not pregnant, do not refer"""
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='NEG', has_record='No', other_record='No')
        HivResultFactory(subject_visit=self.subject_visit_female, hiv_result='Declined')
        ReproductiveHealthFactory(subject_visit=self.subject_visit_female, currently_pregnant='Yes')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertEqual('UNK?-PR', subject_referral.referral_code)

    def tests_referred_pos_female_pregnant(self):
        """if POS and female, pregnant, on-arv, refer ANC-POS"""
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestReviewFactory(subject_visit=self.subject_visit_female, recorded_hiv_result='POS')
        ReproductiveHealthFactory(subject_visit=self.subject_visit_female, currently_pregnant='Yes')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_female, on_arv='Yes')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertIn('POS#-AN', subject_referral.referral_code)

    def tests_referred_pos_female_pregnant2(self):
        """if newly POS and female, and pregnant, refer"""
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_female, hiv_result='POS')
        ReproductiveHealthFactory(subject_visit=self.subject_visit_female, currently_pregnant='Yes')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_female, on_arv='No')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertIn('POS!-PR', subject_referral.referral_code)

    def tests_referred_masa_monitoring1(self):
        """if known POS, on ART,  Cd4 lo, refer as MASA monitoring low"""
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestReviewFactory(subject_visit=self.subject_visit_female, recorded_hiv_result='POS')
        ReproductiveHealthFactory(subject_visit=self.subject_visit_female, currently_pregnant='Yes')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_female, on_arv='No')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertIn('POS#-PR', subject_referral.referral_code)

    def tests_referred_masa_monitoring2(self):
        """if known POS, on ART,  Cd4 hi, refer as MASA monitoring hi"""
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestReviewFactory(subject_visit=self.subject_visit_female, recorded_hiv_result='POS')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_female, on_arv='Yes')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertIn('MASA-CC', subject_referral.referral_code)

    def tests_referred_pos_female_pregnant3(self):
        """if POS and female, and pregnant, refer ANC-POS"""
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_female, hiv_result='POS')
        ReproductiveHealthFactory(subject_visit=self.subject_visit_female, currently_pregnant='Yes')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertIn('POS!-PR', subject_referral.referral_code)

    def tests_referred_neg_female(self):
        """if NEG and female, refer ANC-NEG"""
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_female, hiv_result='NEG')
        ReproductiveHealthFactory(subject_visit=self.subject_visit_female, currently_pregnant='Yes')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertEquals('NEG!-PR', subject_referral.referral_code)

    def tests_referred_cd4(self):
        """if POS but no other data, refer for CD4"""
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('TST-CD4', subject_referral.referral_code)

    def tests_referred1(self):
        """if known POS, high PIMA CD4 and art unknown, """
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestReviewFactory(subject_visit=self.subject_visit_female, recorded_hiv_result='POS', hiv_test_date=date.today())
        PimaFactory(subject_visit=self.subject_visit_female, cd4_value=351, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertIn('POS#-HI', subject_referral.referral_code)

    def tests_referred2(self):
        """if known POS, low PIMA CD4 and art unknown, """
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestReviewFactory(subject_visit=self.subject_visit_female, recorded_hiv_result='POS')
        PimaFactory(subject_visit=self.subject_visit_female, cd4_value=349, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertIn('POS#-LO', subject_referral.referral_code)

    def tests_referred3(self):
        """if known NEG but not tested today, high PIMA CD4 and art unknown, female"""
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestReviewFactory(subject_visit=self.subject_visit_female, recorded_hiv_result='NEG')
        PimaFactory(subject_visit=self.subject_visit_female, cd4_value=351, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertEqual('TST-HIV', subject_referral.referral_code)

    def tests_referred4(self):
        """if new POS, high PIMA CD4 and art unknown, """
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS', hiv_result_datetime=datetime.today())
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=351, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('POS!-HI', subject_referral.referral_code)

    def tests_referred5(self):
        """if new POS, low PIMA CD4 and art unknown, """
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS', hiv_result_datetime=datetime.today())
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=349, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('POS!-LO', subject_referral.referral_code)

    def tests_referred_urgent1(self):
        """if existing POS, low PIMA CD4 and art unknown, urgent referral"""
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestReviewFactory(subject_visit=self.subject_visit_male, recorded_hiv_result='POS')
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=349, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        subject_referral_helper = SubjectReferralHelper(subject_referral)
        self.assertTrue(subject_referral_helper.urgent_referral)

    def tests_referred_urgent2(self):
        """if existing POS, low PIMA CD4 and art no, urgent referral"""
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
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
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS', hiv_result_datetime=datetime.today())
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=349, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        subject_referral_helper = SubjectReferralHelper(subject_referral)
        self.assertTrue(subject_referral_helper.urgent_referral)

    def tests_referred_ccc3(self):
        """if new pos, high PIMA CD4 and not on art, """
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='No')
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=351, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('POS!-HI', subject_referral.referral_code)

    def tests_referred_masa1(self):
        """if new pos, low PIMA CD4 and not on art, """
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='No')
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=349, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('POS!-LO', subject_referral.referral_code)

    def tests_referred_verbal1(self):
        """"""
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='POS', has_record='No', other_record='No')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='No')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('SMC?UNK', subject_referral.referral_code)

    def tests_hiv_result1(self):
        """"""
        self.startup()
        report_datetime = datetime.today()
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='POS', has_record='No', other_record='No')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='Yes', arv_evidence='No')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIsNone(subject_referral.hiv_result)

    def tests_hiv_result2(self):
        """"""
        self.startup()
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
        self.startup()
        base_line_report_datetime = self.subject_visit_male.report_datetime
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male,
                                 report_datetime=base_line_report_datetime,
                                 verbal_hiv_result='POS', has_record='Yes', other_record='No')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male,
                                report_datetime=base_line_report_datetime,
                                on_arv='Yes', arv_evidence='No')
        hiv_test_review = HivTestReviewFactory(
            subject_visit=self.subject_visit_male,
            hiv_test_date=(base_line_report_datetime + timedelta(days=-15)).date(),
            recorded_hiv_result='POS')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=base_line_report_datetime)
        self.assertEqual('POS', subject_referral.hiv_result)
        self.assertEqual(hiv_test_review.hiv_test_date, subject_referral.hiv_result_datetime.date())

        report_datetime = self.subject_visit_male_annual.report_datetime
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male_annual, on_arv='Yes', arv_evidence='No')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male_annual,
            report_datetime=report_datetime)
        self.assertEqual('POS', subject_referral.hiv_result)
        self.assertEqual((base_line_report_datetime + timedelta(days=-15)).date(), subject_referral.hiv_result_datetime.date())
        self.assertEqual(subject_referral.referral_code, 'MASA-CC')
        self.assertTrue(subject_referral.on_art)
        self.assertIsNone(subject_referral.todays_hiv_result)

    def tests_hiv_result3(self):
        """"""
        self.startup()
        base_line_report_datetime = self.subject_visit_male.report_datetime
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male,
                                 report_datetime=base_line_report_datetime,
                                 verbal_hiv_result='POS', has_record='No', other_record='No')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male,
                                report_datetime=base_line_report_datetime,
                                on_arv='No', arv_evidence='Yes')
        hiv_test_review = HivTestReviewFactory(
            subject_visit=self.subject_visit_male,
            hiv_test_date=(base_line_report_datetime + timedelta(days=-15)).date(),
            recorded_hiv_result='POS')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=base_line_report_datetime)
        self.assertEqual('POS', subject_referral.hiv_result)
        self.assertEqual(hiv_test_review.hiv_test_date, subject_referral.hiv_result_datetime.date())

        report_datetime = self.subject_visit_male_annual.report_datetime
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male_annual, on_arv='Yes', arv_evidence='No')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male_annual,
            report_datetime=report_datetime)
        self.assertEqual('POS', subject_referral.hiv_result)
        self.assertEqual((base_line_report_datetime + timedelta(days=-15)).date(), subject_referral.hiv_result_datetime.date())
        self.assertEqual(subject_referral.referral_code, 'MASA-CC')
        self.assertTrue(subject_referral.on_art)

    def tests_hiv_result3a(self):
        """Evidence of being on ARV as reported on Care and Adherence does NOT confirm a verbal positive as evidence of HIV infection"""
        self.startup()
        report_datetime = datetime.today()
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='POS', has_record='No', other_record='No')
        hiv_care_adherence = HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='No', arv_evidence='Yes')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertEqual('POS', subject_referral.hiv_result)
#         print 'subject_referral.hiv_result_datetime = {}'.format(subject_referral.hiv_result_datetime)
        try:
            hiv_result_date = subject_referral.hiv_result_datetime.date()
        except AttributeError:
            hiv_result_date = None
        self.assertEqual(hiv_care_adherence.first_arv, hiv_result_date)

    def tests_hiv_result4(self):
        """Other record confirms a verbal positive as evidence of HIV infection."""
        self.startup()
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

        self.startup()
        report_datetime = datetime.today()
        today_date = date.today()
        last_year_date = today_date - timedelta(days=365)
        HivTestingHistoryFactory(
            subject_visit=self.subject_visit_male,
            verbal_hiv_result='POS',
            has_record='No',
            other_record='Yes')
        HivCareAdherenceFactory(
            subject_visit=self.subject_visit_male, on_arv='No', arv_evidence='No')
        hiv_result_documentation = HivResultDocumentationFactory(
            subject_visit=self.subject_visit_male,
            result_recorded='POS',
            result_date=last_year_date,
            result_doc_type='ART Prescription')
        subject_referral = SubjectStatusHelper(self.subject_visit_male)
        self.assertEqual('POS', subject_referral.hiv_result)
        self.assertFalse(subject_referral.new_pos)
        self.assertTrue(subject_referral.on_art == False)
        # self.assertEqual(hiv_result_documentation.result_date, subject_referral.hiv_result_datetime.date())
        self.assertTrue(ScheduledEntryMetaData.objects.filter(
            appointment=self.subject_visit_male.appointment,
            entry__model_name='hivresult',
            entry_status=NOT_REQUIRED).count() == 1)
        self.assertTrue(ScheduledEntryMetaData.objects.filter(
            appointment=self.subject_visit_male.appointment,
            entry__model_name='pima',
            entry_status=REQUIRED).count() == 1)

    def tests_on_art_always_true_or_false_pos(self):
        """If result is POS then on_art has to take values in [True, False] never None.
        If result is not POS then on_art has to be None as as the other two are not applicable."""
        self.startup()
        base_line_report_datetime = self.subject_visit_male.report_datetime
        testing_history = HivTestingHistoryFactory(subject_visit=self.subject_visit_male,
                                 report_datetime=base_line_report_datetime,
                                 verbal_hiv_result='POS', has_record='No', other_record='No')
        hiv_test_review = HivTestReviewFactory(
            subject_visit=self.subject_visit_male,
            hiv_test_date=(base_line_report_datetime + timedelta(days=-15)).date(),
            recorded_hiv_result='POS')
        care_adherance = HivCareAdherenceFactory(subject_visit=self.subject_visit_male,
                                report_datetime=base_line_report_datetime,
                                on_arv='Yes', arv_evidence='Yes')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=base_line_report_datetime)

        self.assertEqual('POS', subject_referral.hiv_result)
        self.assertTrue(subject_referral.on_art)

        care_adherance.on_arv = 'No'
        care_adherance.arv_evidence = 'No'
        care_adherance.save()

        subject_referral.save()
        self.assertEqual(subject_referral.on_art, False)

        care_adherance.delete()
        self.assertEqual(HivCareAdherence.objects.all().count(), 0)
        hiv_test_review.delete()
        self.assertEqual(HivTestReview.objects.all().count(), 0)
        testing_history.delete()
        self.assertEqual(HivTestingHistory.objects.all().count(), 0)

        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='NEG')

        subject_referral.save()
        self.assertEqual(subject_referral.on_art, None)

    def tests_referred_verbal1b(self):
        """"""
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='POS', other_record='Yes')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='No')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('TST-CD4', subject_referral.referral_code)

    def tests_referred_verbal2(self):
        """"""
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='POS', other_record='Yes')
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='No')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('TST-CD4', subject_referral.referral_code)

    def tests_referred_verbal3(self):
        """"""
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
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
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
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
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='POS', other_record='Yes')
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='Yes')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('MASA-CC', subject_referral.referral_code)

    def tests_referred_verbal6(self):
        """"""
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='POS', other_record='Yes')
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='Yes')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('MASA-CC', subject_referral.referral_code)

    def tests_referred_masa2(self):
        """if new pos, high PIMA CD4 and on art, """
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='Yes')
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=351, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('MASA-CC', subject_referral.referral_code)

    def tests_referred_masa3(self):
        """if pos, low CD4 and on art, """
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='Yes')
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=350, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('MASA-CC', subject_referral.referral_code)

    def tests_referred_masa4(self):
        """Tests pos today but have evidence on ART"""
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv='No', arv_evidence='Yes')
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=350, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('MASA-DF', subject_referral.referral_code)

    def tests_referred_masa5(self):
        """if pos and defaulter """
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestReviewFactory(subject_visit=self.subject_visit_female, recorded_hiv_result='POS')
        HivCareAdherenceFactory(subject_visit=self.subject_visit_female, on_arv='No', arv_evidence='Yes')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertIn('MASA-DF', subject_referral.referral_code)

    def tests_subject_referral_field_attr1(self):
        self.startup()
        report_datetime = self.subject_visit_female.report_datetime
        last_year_date = self.subject_visit_female.report_datetime - timedelta(days=365)
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(
            subject_visit=self.subject_visit_female,
            site=self.study_site,
            is_drawn='Yes',
            panel=panel,
            aliquot_type=AliquotType.objects.get(alpha_code='WB'),
            drawn_datetime=self.subject_visit_female.report_datetime)
        HivResultFactory(
            subject_visit=self.subject_visit_female,
            hiv_result='POS',
            hiv_result_datetime=self.subject_visit_female.report_datetime,
            report_datetime=self.subject_visit_female.report_datetime)
        HivTestReviewFactory(subject_visit=self.subject_visit_female, recorded_hiv_result='POS', hiv_test_date=last_year_date)
        HivCareAdherenceFactory(subject_visit=self.subject_visit_female, on_arv='Yes', arv_evidence='Yes')
        if site_mappers.current_mapper().current_survey_slug == BASELINE_SURVEY_SLUG:
            TbSymptomsFactory(subject_visit=self.subject_visit_female)
            PimaFactory(subject_visit=self.subject_visit_female, cd4_value=350, report_datetime=report_datetime, cd4_datetime=self.subject_visit_female.report_datetime)
        panel = Panel.objects.get(name='Viral Load')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.study_site, is_drawn='Yes', panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'), drawn_datetime=self.subject_visit_female.report_datetime)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime,
            referral_clinic=site_mappers.current_mapper().map_area,
            )
        subject_referral_helper = SubjectReferralHelper(subject_referral)
        expected = {
            'arv_documentation': True,
            'arv_clinic': None,
            'cd4_result': 350,
            'cd4_result_datetime': self.subject_visit_female.report_datetime,
            'circumcised': None,
            'citizen': True,
            'citizen_spouse': False,
            'direct_hiv_documentation': True,
            'gender': u'F',
            'hiv_result': u'POS',
            'hiv_result_datetime': last_year_date.date(),
            'indirect_hiv_documentation': None,
            'last_hiv_result': u'POS',
            'new_pos': False,
            'next_arv_clinic_appointment_date': None,
            'on_art': True,
            'permanent_resident': None,
            'pregnant': None,
            'referral_clinic': site_mappers.current_mapper().map_area,
            'referral_code': 'MASA-CC',
            'tb_symptoms': 'cough, cough_blood, night_sweat',
            'urgent_referral': False,
            'verbal_hiv_result': None,
            'vl_sample_drawn': True,
            'vl_sample_drawn_datetime': self.subject_visit_female.report_datetime}
        if site_mappers.current_mapper().current_survey_slug != BASELINE_SURVEY_SLUG:
            del expected['cd4_result']
            del expected['cd4_result_datetime']
            del expected['tb_symptoms']
        subject_referral_helper.subject_referral_dict['hiv_result_datetime'] = subject_referral_helper.subject_referral_dict['hiv_result_datetime'].date()
        self.assertDictContainsSubset(expected, subject_referral_helper.subject_referral_dict)

    def tests_subject_referral_field_attr2(self):
        self.startup()
        report_datetime = datetime.today()
        today = datetime.today()
        today_date = date.today()
        last_year_date = today_date - timedelta(days=365)
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.study_site, is_drawn='Yes', panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'), drawn_datetime=datetime.today())
        TbSymptomsFactory(subject_visit=self.subject_visit_female)
        # verbal POS with indirect docs
        HivTestingHistoryFactory(subject_visit=self.subject_visit_female, verbal_hiv_result='POS', has_record='No', other_record='Yes')
        #
        HivResultDocumentationFactory(subject_visit=self.subject_visit_female, result_recorded='POS', result_date=last_year_date, result_doc_type='ART Prescription')
        # on ART and there are docs 
        HivCareAdherenceFactory(subject_visit=self.subject_visit_female, on_arv='Yes', arv_evidence='Yes')
        panel = Panel.objects.get(name='Viral Load')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.study_site, is_drawn='Yes', panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'), drawn_datetime=today)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime,
            referral_clinic=site_mappers.current_mapper().map_area)
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
            'referral_clinic': site_mappers.current_mapper().map_area,
            'referral_code': 'MASA-CC',
            'tb_symptoms': 'cough, cough_blood, night_sweat',
            'urgent_referral': False,
            'verbal_hiv_result': 'POS',
            'vl_sample_drawn': True,
            'vl_sample_drawn_datetime': today}
        self.assertDictContainsSubset(expected, subject_referral_helper.subject_referral_dict)

    def tests_subject_referral_field_attr3(self):
        self.startup()
        yesterday = self.subject_visit_female.report_datetime - timedelta(days=1)
        report_datetime = datetime.today()
        today = datetime.today()
        today_date = date.today()
        last_year_date = today_date - timedelta(days=365)
        panel = Panel.objects.get(name='Microtube')
        self.subject_visit_female.report_datetime = yesterday
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.study_site, is_drawn='Yes', panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'), drawn_datetime=yesterday)
        # verbal POS with indirect docs
        HivTestingHistoryFactory(subject_visit=self.subject_visit_female, report_datetime=yesterday, verbal_hiv_result='POS', has_record='No', other_record='Yes')
        # on ART and there are docs hence indirect documentations
        HivCareAdherenceFactory(subject_visit=self.subject_visit_female, report_datetime=yesterday, ever_taken_arv='Yes', on_arv='No', arv_stop_date=last_year_date, arv_evidence='Yes')

        panel = Panel.objects.get(name='Viral Load')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.study_site, is_drawn='Yes', panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'), drawn_datetime=yesterday)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime,
            referral_clinic=site_mappers.current_mapper().map_area)
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
            'last_hiv_result': 'POS',
            'new_pos': False,
            'next_arv_clinic_appointment_date': None,
            'on_art': True,
            'permanent_resident': None,
            'pregnant': None,
            'referral_clinic': site_mappers.current_mapper().map_area,
            'referral_code': 'MASA-DF',
            'tb_symptoms': '',
            'urgent_referral': True,
            'verbal_hiv_result': 'POS',
            'vl_sample_drawn': True,
            'vl_sample_drawn_datetime': yesterday}
        self.assertDictContainsSubset(expected, subject_referral_helper.subject_referral_dict)

    def tests_subject_referral_field_attr4(self):
        self.startup()
        yesterday = self.subject_visit_female.report_datetime - timedelta(days=1)
        first_arv = self.subject_visit_female.report_datetime - timedelta(days=120)
        report_datetime = datetime.today()
        today = datetime.today()
        today_date = date.today()
        last_year_date = today_date - timedelta(days=365)
        panel = Panel.objects.get(name='Microtube')
        self.subject_visit_female.report_datetime = yesterday
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.study_site, is_drawn='Yes', panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'), drawn_datetime=yesterday)
        # verbal POS with indirect docs
        HivTestingHistoryFactory(subject_visit=self.subject_visit_female, report_datetime=yesterday, verbal_hiv_result='POS', has_record='No', other_record='No')
        # on ART and there are docs 
        HivCareAdherenceFactory(subject_visit=self.subject_visit_female, report_datetime=yesterday, ever_taken_arv='Yes', on_arv='No', arv_stop_date=last_year_date, arv_evidence='Yes',
                                first_arv=first_arv.date())
#         hiv_result_options = {}
#         hiv_result_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='hivresult',
#             appointment=self.subject_visit_female.appointment)
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NOT_REQUIRED', **hiv_result_options).count(), 1)
        #HivResultFactory(subject_visit=self.subject_visit_female, hiv_result='POS', hiv_result_datetime=yesterday)
        panel = Panel.objects.get(name='Viral Load')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.study_site, is_drawn='Yes', panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'), drawn_datetime=yesterday)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime,
            referral_clinic=site_mappers.current_mapper().map_area)
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
            'hiv_result_datetime': first_arv.replace(hour=0, minute=0, second=0, microsecond=0),
            'indirect_hiv_documentation': True,
            'last_hiv_result': 'POS',
            'new_pos': False,  # undocumented verbal_hiv_result can suggest not a new POS
            'next_arv_clinic_appointment_date': None,
            'on_art': True,
            'permanent_resident': None,
            'pregnant': None,
            'referral_clinic': site_mappers.current_mapper().map_area,
            'referral_code': 'MASA-DF',
            'tb_symptoms': '',
            'urgent_referral': True,  # because this is a defaulter
            'verbal_hiv_result': 'POS',
            'vl_sample_drawn': True,
            'vl_sample_drawn_datetime': yesterday}
        self.assertDictContainsSubset(expected, subject_referral_helper.subject_referral_dict)

    def tests_subject_referral_field_attr5(self):
        """if IND refer for HIV testing"""
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
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
        self.assertDictContainsSubset(expected, subject_referral_helper.subject_referral_dict)

    def tests_subject_referral_field_attr6(self):
        """if IND refer for HIV testing"""
        self.startup()
        report_datetime = datetime.today()
        last_date = report_datetime.date() - relativedelta(years=3)
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='POS', has_record='Yes', other_record='No')
        HivTestReviewFactory(subject_visit=self.subject_visit_male, hiv_test_date=last_date, recorded_hiv_result='NEG')
        #HivResultDocumentationFactory(subject_visit=self.subject_visit_male, result_date=report_datetime - relativedelta(years=1), result_recorded='POS', result_doc_type='Record of CD4 count')
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='Declined')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        subject_referral_helper = SubjectReferralHelper(subject_referral)
        expected = {
            'direct_hiv_documentation': True,
            'indirect_hiv_documentation': False,
            'last_hiv_result': 'NEG',
            'last_hiv_result_date': last_date,
            'new_pos': None,
            'verbal_hiv_result': 'POS',
            'hiv_result': None}
        self.assertDictContainsSubset(expected, subject_referral_helper.subject_referral_dict)

    def tests_subject_referral_field_attr7(self):
        """ """
        self.startup()
        report_datetime = datetime.today()
        last_date = report_datetime.date() - relativedelta(years=3)
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='POS', has_record='Yes', other_record='Yes')
        HivTestReviewFactory(subject_visit=self.subject_visit_male, hiv_test_date=last_date, recorded_hiv_result='NEG')
        HivResultDocumentationFactory(subject_visit=self.subject_visit_male, result_date=report_datetime - relativedelta(years=1), result_recorded='POS', result_doc_type='Record of CD4 count')
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='Declined')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        subject_referral_helper = SubjectReferralHelper(subject_referral)
        expected = {
            'direct_hiv_documentation': True,
            'indirect_hiv_documentation': True,
            'last_hiv_result': 'NEG',
            'last_hiv_result_date': last_date,
            'new_pos': False,
            'verbal_hiv_result': 'POS',
            'hiv_result': 'POS'}
        self.assertDictContainsSubset(expected, subject_referral_helper.subject_referral_dict)

    def tests_subject_referral_field_attr8(self):
        """ """
        self.startup()
        report_datetime = datetime.today()
        last_date = report_datetime.date() - relativedelta(years=3)
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
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
        self.assertDictContainsSubset(expected, subject_referral_helper.subject_referral_dict)

    def tests_subject_referral_field_attr9(self):
        """ """
        self.startup()
        report_datetime = datetime.today()
        #last_date = report_datetime.date() - relativedelta(years=3)
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
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
#             'last_hiv_result': None,
            'last_hiv_result': 'POS',
            'last_hiv_result_date': None,
            'new_pos': False,
            'verbal_hiv_result': 'POS',
            'hiv_result': 'POS'}
        self.assertDictContainsSubset(expected, subject_referral_helper.subject_referral_dict)

    def test_export_history1(self):
        """Asserts a referral is queued for export."""
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='NEG')
        CircumcisionFactory(subject_visit=self.subject_visit_male, circumcised='No')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('SMC-NEG', subject_referral.referral_code)
        self.assertEqual(ExportTransaction.objects.filter(tx_pk=subject_referral.pk).count(), 1)

    def tests_new_pos_evaluated_correctly_in_annual(self):
        """Test that new_pos field in referral is evaluated correctly in y2."""
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS', hiv_result_datetime=datetime.today())
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=349, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertTrue(subject_referral.new_pos)
        subject_referral_annual = SubjectReferralFactory(
            subject_visit=self.subject_visit_male_annual,
            report_datetime=report_datetime)
        self.assertFalse(subject_referral_annual.new_pos)

    def tests_correctness_of_citizen_field(self):
        """Asserts that a citizen field is populated correctly following enrollment_checklist value."""
        self.startup()
        report_datetime = datetime.today()
        #last_date = report_datetime.date() - relativedelta(years=3)
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='POS', has_record='Yes', other_record='Yes')
        #HivTestReviewFactory(subject_visit=self.subject_visit_male, hiv_test_date=last_date, recorded_hiv_result='POS')
        #HivResultDocumentationFactory(subject_visit=self.subject_visit_male, result_date=report_datetime - relativedelta(years=1), result_recorded='POS', result_doc_type='Record of CD4 count')
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='POS')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertTrue(subject_referral.citizen)

        non_citizen_household_member_male = HouseholdMemberFactory(household_structure=self.household_structure,
                                                            first_name='ONEP', initials='OP', gender='M',
                                                            age_in_years=30, study_resident='Yes', relation='brother',
                                                            inability_to_participate=NOT_APPLICABLE)

        non_citizen_enrollment_male = EnrollmentChecklistFactory(
            household_member=non_citizen_household_member_male,
            initials=non_citizen_household_member_male.initials,
            gender=non_citizen_household_member_male.gender,
            dob=date.today() - relativedelta(years=non_citizen_household_member_male.age_in_years),
            guardian=NOT_APPLICABLE,
            part_time_resident='Yes',
            citizen='No',
            legal_marriage='Yes',
            marriage_certificate='Yes')

        non_citizen_subject_consent_male = SubjectConsentFactory(
            consent_datetime=datetime.today() + relativedelta(years=-1),
            household_member=non_citizen_household_member_male,
            gender='M',
            dob=non_citizen_enrollment_male.dob,
            first_name='ONEP',
            last_name='PH',
            citizen='No',
            initials=non_citizen_enrollment_male.initials,
            legal_marriage='Yes',
            marriage_certificate='Yes',
            marriage_certificate_no='9999776',
            study_site=self.study_site)

        non_citizen_appointment_male = Appointment.objects.get(registered_subject=non_citizen_subject_consent_male.registered_subject,
                                                               visit_definition__time_point=0)

        non_citizen_subject_visit_male = SubjectVisitFactory(
            report_datetime=datetime.today() + relativedelta(years=-1),
            appointment=non_citizen_appointment_male, household_member=non_citizen_household_member_male)
        SubjectLocatorFactory(subject_visit=non_citizen_subject_visit_male)
        SubjectRequisitionFactory(subject_visit=non_citizen_subject_visit_male, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestingHistoryFactory(subject_visit=non_citizen_subject_visit_male, verbal_hiv_result='POS', has_record='Yes', other_record='Yes')
        HivResultFactory(subject_visit=non_citizen_subject_visit_male, hiv_result='POS')
        subject_referral = SubjectReferralFactory(
            subject_visit=non_citizen_subject_visit_male,
            report_datetime=report_datetime)
        self.assertFalse(subject_referral.citizen)
