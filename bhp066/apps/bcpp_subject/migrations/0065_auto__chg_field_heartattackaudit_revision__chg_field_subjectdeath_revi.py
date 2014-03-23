# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'HeartAttackAudit.revision'
        db.alter_column(u'bcpp_subject_heartattack_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'SubjectDeath.revision'
        db.alter_column(u'bcpp_subject_subjectdeath', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'HivHealthCareCostsAudit.revision'
        db.alter_column(u'bcpp_subject_hivhealthcarecosts_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'PositiveParticipantAudit.revision'
        db.alter_column(u'bcpp_subject_positiveparticipant_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'Circumcised.revision'
        db.alter_column(u'bcpp_subject_circumcised', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'OutpatientCareAudit.revision'
        db.alter_column(u'bcpp_subject_outpatientcare_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'Cd4History.revision'
        db.alter_column(u'bcpp_subject_cd4history', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'Stigma.revision'
        db.alter_column(u'bcpp_subject_stigma', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'Pregnancy.revision'
        db.alter_column(u'bcpp_subject_pregnancy', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'NonPregnancyAudit.revision'
        db.alter_column(u'bcpp_subject_nonpregnancy_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'SubjectOffStudyAudit.revision'
        db.alter_column(u'bcpp_subject_subjectoffstudy_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'HivUntestedAudit.revision'
        db.alter_column(u'bcpp_subject_hivuntested_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'CommunityEngagement.revision'
        db.alter_column(u'bcpp_subject_communityengagement', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'SubjectDeathAudit.revision'
        db.alter_column(u'bcpp_subject_subjectdeath_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'Demographics.revision'
        db.alter_column(u'bcpp_subject_demographics', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'LabourMarketWagesAudit.revision'
        db.alter_column(u'bcpp_subject_labourmarketwages_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'MonthsRecentPartnerAudit.revision'
        db.alter_column(u'bcpp_subject_monthsrecentpartner_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'SubjectReferral.revision'
        db.alter_column(u'bcpp_subject_subjectreferral', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'QualityOfLife.revision'
        db.alter_column(u'bcpp_subject_qualityoflife', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'SubjectConsentAudit.revision'
        db.alter_column(u'bcpp_subject_subjectconsent_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'CeaEnrollmentChecklist.revision'
        db.alter_column(u'bcpp_subject_ceaenrollmentchecklist', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'FutureHivTesting.revision'
        db.alter_column(u'bcpp_subject_futurehivtesting', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'PositiveParticipant.revision'
        db.alter_column(u'bcpp_subject_positiveparticipant', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'TubercolosisAudit.revision'
        db.alter_column(u'bcpp_subject_tubercolosis_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'Pima.revision'
        db.alter_column(u'bcpp_subject_pima', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'Grant.revision'
        db.alter_column(u'bcpp_subject_grant', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'SubjectConsent.revision'
        db.alter_column(u'bcpp_subject_subjectconsent', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'Uncircumcised.revision'
        db.alter_column(u'bcpp_subject_uncircumcised', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'Cancer.revision'
        db.alter_column(u'bcpp_subject_cancer', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'SubjectLocatorAudit.revision'
        db.alter_column(u'bcpp_subject_subjectlocator_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'HivTestingHistory.revision'
        db.alter_column(u'bcpp_subject_hivtestinghistory', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'HivResultAudit.revision'
        db.alter_column(u'bcpp_subject_hivresult_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'HivResultDocumentation.revision'
        db.alter_column(u'bcpp_subject_hivresultdocumentation', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'MonthsSecondPartnerAudit.revision'
        db.alter_column(u'bcpp_subject_monthssecondpartner_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'SubjectReferralAudit.revision'
        db.alter_column(u'bcpp_subject_subjectreferral_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'ResourceUtilization.revision'
        db.alter_column(u'bcpp_subject_resourceutilization', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'AccessToCare.revision'
        db.alter_column(u'bcpp_subject_accesstocare', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'PimaAudit.revision'
        db.alter_column(u'bcpp_subject_pima_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'HeartAttack.revision'
        db.alter_column(u'bcpp_subject_heartattack', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'StigmaOpinionAudit.revision'
        db.alter_column(u'bcpp_subject_stigmaopinion_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'HivUntested.revision'
        db.alter_column(u'bcpp_subject_hivuntested', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'MonthsThirdPartnerAudit.revision'
        db.alter_column(u'bcpp_subject_monthsthirdpartner_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'HivTestReviewAudit.revision'
        db.alter_column(u'bcpp_subject_hivtestreview_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'HivMedicalCareAudit.revision'
        db.alter_column(u'bcpp_subject_hivmedicalcare_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'HospitalAdmissionAudit.revision'
        db.alter_column(u'bcpp_subject_hospitaladmission_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'SubjectVisitAudit.revision'
        db.alter_column(u'bcpp_subject_subjectvisit_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'MonthsThirdPartner.revision'
        db.alter_column(u'bcpp_subject_monthsthirdpartner', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'ReproductiveHealth.revision'
        db.alter_column(u'bcpp_subject_reproductivehealth', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'FutureHivTestingAudit.revision'
        db.alter_column(u'bcpp_subject_futurehivtesting_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'Sti.revision'
        db.alter_column(u'bcpp_subject_sti', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'Circumcision.revision'
        db.alter_column(u'bcpp_subject_circumcision', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'CircumcisedAudit.revision'
        db.alter_column(u'bcpp_subject_circumcised_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'ResidencyMobility.revision'
        db.alter_column(u'bcpp_subject_residencymobility', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'ResourceUtilizationAudit.revision'
        db.alter_column(u'bcpp_subject_resourceutilization_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'AccessToCareAudit.revision'
        db.alter_column(u'bcpp_subject_accesstocare_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'StigmaAudit.revision'
        db.alter_column(u'bcpp_subject_stigma_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'CancerAudit.revision'
        db.alter_column(u'bcpp_subject_cancer_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'HivCareAdherence.revision'
        db.alter_column(u'bcpp_subject_hivcareadherence', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'HivHealthCareCosts.revision'
        db.alter_column(u'bcpp_subject_hivhealthcarecosts', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'MonthsRecentPartner.revision'
        db.alter_column(u'bcpp_subject_monthsrecentpartner', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'PregnancyAudit.revision'
        db.alter_column(u'bcpp_subject_pregnancy_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Deleting field 'MedicalDiagnoses.cancer_record_comment'
        db.delete_column(u'bcpp_subject_medicaldiagnoses', 'cancer_record_comment')

        # Deleting field 'MedicalDiagnoses.tb_record_comment'
        db.delete_column(u'bcpp_subject_medicaldiagnoses', 'tb_record_comment')

        # Deleting field 'MedicalDiagnoses.heart_attack_comment'
        db.delete_column(u'bcpp_subject_medicaldiagnoses', 'heart_attack_comment')

        # Changing field 'MedicalDiagnoses.revision'
        db.alter_column(u'bcpp_subject_medicaldiagnoses', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'CircumcisionAudit.revision'
        db.alter_column(u'bcpp_subject_circumcision_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'SubstanceUse.revision'
        db.alter_column(u'bcpp_subject_substanceuse', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'StiAudit.revision'
        db.alter_column(u'bcpp_subject_sti_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'ReproductiveHealthAudit.revision'
        db.alter_column(u'bcpp_subject_reproductivehealth_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'HivResult.revision'
        db.alter_column(u'bcpp_subject_hivresult', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'OutpatientCare.revision'
        db.alter_column(u'bcpp_subject_outpatientcare', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'GrantAudit.revision'
        db.alter_column(u'bcpp_subject_grant_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'HivTestReview.revision'
        db.alter_column(u'bcpp_subject_hivtestreview', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'ResidencyMobilityAudit.revision'
        db.alter_column(u'bcpp_subject_residencymobility_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'MonthsSecondPartner.revision'
        db.alter_column(u'bcpp_subject_monthssecondpartner', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'ClinicQuestionnaireAudit.revision'
        db.alter_column(u'bcpp_subject_clinicquestionnaire_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'SubjectOffStudy.revision'
        db.alter_column(u'bcpp_subject_subjectoffstudy', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'SubjectVisit.revision'
        db.alter_column(u'bcpp_subject_subjectvisit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'SubstanceUseAudit.revision'
        db.alter_column(u'bcpp_subject_substanceuse_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'SubjectConsentHistory.revision'
        db.alter_column(u'bcpp_subject_subjectconsenthistory', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'HivCareAdherenceAudit.revision'
        db.alter_column(u'bcpp_subject_hivcareadherence_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'Tubercolosis.revision'
        db.alter_column(u'bcpp_subject_tubercolosis', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'CommunityEngagementAudit.revision'
        db.alter_column(u'bcpp_subject_communityengagement_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'SexualBehaviourAudit.revision'
        db.alter_column(u'bcpp_subject_sexualbehaviour_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'SubjectConsentRbd.revision'
        db.alter_column(u'bcpp_subject_subjectconsentrbd', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'CeaEnrollmentChecklistAudit.revision'
        db.alter_column(u'bcpp_subject_ceaenrollmentchecklist_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'HivMedicalCare.revision'
        db.alter_column(u'bcpp_subject_hivmedicalcare', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'StigmaOpinion.revision'
        db.alter_column(u'bcpp_subject_stigmaopinion', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'Education.revision'
        db.alter_column(u'bcpp_subject_education', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'QualityOfLifeAudit.revision'
        db.alter_column(u'bcpp_subject_qualityoflife_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'SubjectConsentRbdAudit.revision'
        db.alter_column(u'bcpp_subject_subjectconsentrbd_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'HivResultDocumentationAudit.revision'
        db.alter_column(u'bcpp_subject_hivresultdocumentation_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'SexualBehaviour.revision'
        db.alter_column(u'bcpp_subject_sexualbehaviour', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'DemographicsAudit.revision'
        db.alter_column(u'bcpp_subject_demographics_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'HivTestingHistoryAudit.revision'
        db.alter_column(u'bcpp_subject_hivtestinghistory_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'ClinicQuestionnaire.revision'
        db.alter_column(u'bcpp_subject_clinicquestionnaire', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'Cd4HistoryAudit.revision'
        db.alter_column(u'bcpp_subject_cd4history_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'SubjectLocator.revision'
        db.alter_column(u'bcpp_subject_subjectlocator', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'HospitalAdmission.revision'
        db.alter_column(u'bcpp_subject_hospitaladmission', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'HivTestedAudit.revision'
        db.alter_column(u'bcpp_subject_hivtested_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'NonPregnancy.revision'
        db.alter_column(u'bcpp_subject_nonpregnancy', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'UncircumcisedAudit.revision'
        db.alter_column(u'bcpp_subject_uncircumcised_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'LabourMarketWages.revision'
        db.alter_column(u'bcpp_subject_labourmarketwages', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'EducationAudit.revision'
        db.alter_column(u'bcpp_subject_education_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Deleting field 'MedicalDiagnosesAudit.cancer_record_comment'
        db.delete_column(u'bcpp_subject_medicaldiagnoses_audit', 'cancer_record_comment')

        # Deleting field 'MedicalDiagnosesAudit.heart_attack_comment'
        db.delete_column(u'bcpp_subject_medicaldiagnoses_audit', 'heart_attack_comment')

        # Deleting field 'MedicalDiagnosesAudit.tb_record_comment'
        db.delete_column(u'bcpp_subject_medicaldiagnoses_audit', 'tb_record_comment')

        # Changing field 'MedicalDiagnosesAudit.revision'
        db.alter_column(u'bcpp_subject_medicaldiagnoses_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'HivTested.revision'
        db.alter_column(u'bcpp_subject_hivtested', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

    def backwards(self, orm):

        # Changing field 'HeartAttackAudit.revision'
        db.alter_column(u'bcpp_subject_heartattack_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'SubjectDeath.revision'
        db.alter_column(u'bcpp_subject_subjectdeath', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'HivHealthCareCostsAudit.revision'
        db.alter_column(u'bcpp_subject_hivhealthcarecosts_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'PositiveParticipantAudit.revision'
        db.alter_column(u'bcpp_subject_positiveparticipant_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Circumcised.revision'
        db.alter_column(u'bcpp_subject_circumcised', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'OutpatientCareAudit.revision'
        db.alter_column(u'bcpp_subject_outpatientcare_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Cd4History.revision'
        db.alter_column(u'bcpp_subject_cd4history', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Stigma.revision'
        db.alter_column(u'bcpp_subject_stigma', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Pregnancy.revision'
        db.alter_column(u'bcpp_subject_pregnancy', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'NonPregnancyAudit.revision'
        db.alter_column(u'bcpp_subject_nonpregnancy_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'SubjectOffStudyAudit.revision'
        db.alter_column(u'bcpp_subject_subjectoffstudy_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'HivUntestedAudit.revision'
        db.alter_column(u'bcpp_subject_hivuntested_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'CommunityEngagement.revision'
        db.alter_column(u'bcpp_subject_communityengagement', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'SubjectDeathAudit.revision'
        db.alter_column(u'bcpp_subject_subjectdeath_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Demographics.revision'
        db.alter_column(u'bcpp_subject_demographics', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'LabourMarketWagesAudit.revision'
        db.alter_column(u'bcpp_subject_labourmarketwages_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'MonthsRecentPartnerAudit.revision'
        db.alter_column(u'bcpp_subject_monthsrecentpartner_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'SubjectReferral.revision'
        db.alter_column(u'bcpp_subject_subjectreferral', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'QualityOfLife.revision'
        db.alter_column(u'bcpp_subject_qualityoflife', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'SubjectConsentAudit.revision'
        db.alter_column(u'bcpp_subject_subjectconsent_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'CeaEnrollmentChecklist.revision'
        db.alter_column(u'bcpp_subject_ceaenrollmentchecklist', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'FutureHivTesting.revision'
        db.alter_column(u'bcpp_subject_futurehivtesting', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'PositiveParticipant.revision'
        db.alter_column(u'bcpp_subject_positiveparticipant', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'TubercolosisAudit.revision'
        db.alter_column(u'bcpp_subject_tubercolosis_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Pima.revision'
        db.alter_column(u'bcpp_subject_pima', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Grant.revision'
        db.alter_column(u'bcpp_subject_grant', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'SubjectConsent.revision'
        db.alter_column(u'bcpp_subject_subjectconsent', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Uncircumcised.revision'
        db.alter_column(u'bcpp_subject_uncircumcised', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Cancer.revision'
        db.alter_column(u'bcpp_subject_cancer', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'SubjectLocatorAudit.revision'
        db.alter_column(u'bcpp_subject_subjectlocator_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'HivTestingHistory.revision'
        db.alter_column(u'bcpp_subject_hivtestinghistory', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'HivResultAudit.revision'
        db.alter_column(u'bcpp_subject_hivresult_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'HivResultDocumentation.revision'
        db.alter_column(u'bcpp_subject_hivresultdocumentation', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'MonthsSecondPartnerAudit.revision'
        db.alter_column(u'bcpp_subject_monthssecondpartner_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'SubjectReferralAudit.revision'
        db.alter_column(u'bcpp_subject_subjectreferral_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'ResourceUtilization.revision'
        db.alter_column(u'bcpp_subject_resourceutilization', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'AccessToCare.revision'
        db.alter_column(u'bcpp_subject_accesstocare', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'PimaAudit.revision'
        db.alter_column(u'bcpp_subject_pima_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'HeartAttack.revision'
        db.alter_column(u'bcpp_subject_heartattack', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'StigmaOpinionAudit.revision'
        db.alter_column(u'bcpp_subject_stigmaopinion_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'HivUntested.revision'
        db.alter_column(u'bcpp_subject_hivuntested', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'MonthsThirdPartnerAudit.revision'
        db.alter_column(u'bcpp_subject_monthsthirdpartner_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'HivTestReviewAudit.revision'
        db.alter_column(u'bcpp_subject_hivtestreview_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'HivMedicalCareAudit.revision'
        db.alter_column(u'bcpp_subject_hivmedicalcare_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'HospitalAdmissionAudit.revision'
        db.alter_column(u'bcpp_subject_hospitaladmission_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'SubjectVisitAudit.revision'
        db.alter_column(u'bcpp_subject_subjectvisit_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'MonthsThirdPartner.revision'
        db.alter_column(u'bcpp_subject_monthsthirdpartner', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'ReproductiveHealth.revision'
        db.alter_column(u'bcpp_subject_reproductivehealth', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'FutureHivTestingAudit.revision'
        db.alter_column(u'bcpp_subject_futurehivtesting_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Sti.revision'
        db.alter_column(u'bcpp_subject_sti', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Circumcision.revision'
        db.alter_column(u'bcpp_subject_circumcision', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'CircumcisedAudit.revision'
        db.alter_column(u'bcpp_subject_circumcised_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'ResidencyMobility.revision'
        db.alter_column(u'bcpp_subject_residencymobility', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'ResourceUtilizationAudit.revision'
        db.alter_column(u'bcpp_subject_resourceutilization_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'AccessToCareAudit.revision'
        db.alter_column(u'bcpp_subject_accesstocare_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'StigmaAudit.revision'
        db.alter_column(u'bcpp_subject_stigma_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'CancerAudit.revision'
        db.alter_column(u'bcpp_subject_cancer_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'HivCareAdherence.revision'
        db.alter_column(u'bcpp_subject_hivcareadherence', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'HivHealthCareCosts.revision'
        db.alter_column(u'bcpp_subject_hivhealthcarecosts', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'MonthsRecentPartner.revision'
        db.alter_column(u'bcpp_subject_monthsrecentpartner', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'PregnancyAudit.revision'
        db.alter_column(u'bcpp_subject_pregnancy_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Adding field 'MedicalDiagnoses.cancer_record_comment'
        db.add_column(u'bcpp_subject_medicaldiagnoses', 'cancer_record_comment',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'MedicalDiagnoses.tb_record_comment'
        db.add_column(u'bcpp_subject_medicaldiagnoses', 'tb_record_comment',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'MedicalDiagnoses.heart_attack_comment'
        db.add_column(u'bcpp_subject_medicaldiagnoses', 'heart_attack_comment',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Changing field 'MedicalDiagnoses.revision'
        db.alter_column(u'bcpp_subject_medicaldiagnoses', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'CircumcisionAudit.revision'
        db.alter_column(u'bcpp_subject_circumcision_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'SubstanceUse.revision'
        db.alter_column(u'bcpp_subject_substanceuse', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'StiAudit.revision'
        db.alter_column(u'bcpp_subject_sti_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'ReproductiveHealthAudit.revision'
        db.alter_column(u'bcpp_subject_reproductivehealth_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'HivResult.revision'
        db.alter_column(u'bcpp_subject_hivresult', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'OutpatientCare.revision'
        db.alter_column(u'bcpp_subject_outpatientcare', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'GrantAudit.revision'
        db.alter_column(u'bcpp_subject_grant_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'HivTestReview.revision'
        db.alter_column(u'bcpp_subject_hivtestreview', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'ResidencyMobilityAudit.revision'
        db.alter_column(u'bcpp_subject_residencymobility_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'MonthsSecondPartner.revision'
        db.alter_column(u'bcpp_subject_monthssecondpartner', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'ClinicQuestionnaireAudit.revision'
        db.alter_column(u'bcpp_subject_clinicquestionnaire_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'SubjectOffStudy.revision'
        db.alter_column(u'bcpp_subject_subjectoffstudy', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'SubjectVisit.revision'
        db.alter_column(u'bcpp_subject_subjectvisit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'SubstanceUseAudit.revision'
        db.alter_column(u'bcpp_subject_substanceuse_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'SubjectConsentHistory.revision'
        db.alter_column(u'bcpp_subject_subjectconsenthistory', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'HivCareAdherenceAudit.revision'
        db.alter_column(u'bcpp_subject_hivcareadherence_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Tubercolosis.revision'
        db.alter_column(u'bcpp_subject_tubercolosis', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'CommunityEngagementAudit.revision'
        db.alter_column(u'bcpp_subject_communityengagement_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'SexualBehaviourAudit.revision'
        db.alter_column(u'bcpp_subject_sexualbehaviour_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'SubjectConsentRbd.revision'
        db.alter_column(u'bcpp_subject_subjectconsentrbd', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'CeaEnrollmentChecklistAudit.revision'
        db.alter_column(u'bcpp_subject_ceaenrollmentchecklist_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'HivMedicalCare.revision'
        db.alter_column(u'bcpp_subject_hivmedicalcare', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'StigmaOpinion.revision'
        db.alter_column(u'bcpp_subject_stigmaopinion', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Education.revision'
        db.alter_column(u'bcpp_subject_education', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'QualityOfLifeAudit.revision'
        db.alter_column(u'bcpp_subject_qualityoflife_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'SubjectConsentRbdAudit.revision'
        db.alter_column(u'bcpp_subject_subjectconsentrbd_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'HivResultDocumentationAudit.revision'
        db.alter_column(u'bcpp_subject_hivresultdocumentation_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'SexualBehaviour.revision'
        db.alter_column(u'bcpp_subject_sexualbehaviour', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'DemographicsAudit.revision'
        db.alter_column(u'bcpp_subject_demographics_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'HivTestingHistoryAudit.revision'
        db.alter_column(u'bcpp_subject_hivtestinghistory_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'ClinicQuestionnaire.revision'
        db.alter_column(u'bcpp_subject_clinicquestionnaire', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Cd4HistoryAudit.revision'
        db.alter_column(u'bcpp_subject_cd4history_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'SubjectLocator.revision'
        db.alter_column(u'bcpp_subject_subjectlocator', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'HospitalAdmission.revision'
        db.alter_column(u'bcpp_subject_hospitaladmission', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'HivTestedAudit.revision'
        db.alter_column(u'bcpp_subject_hivtested_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'NonPregnancy.revision'
        db.alter_column(u'bcpp_subject_nonpregnancy', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'UncircumcisedAudit.revision'
        db.alter_column(u'bcpp_subject_uncircumcised_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'LabourMarketWages.revision'
        db.alter_column(u'bcpp_subject_labourmarketwages', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'EducationAudit.revision'
        db.alter_column(u'bcpp_subject_education_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Adding field 'MedicalDiagnosesAudit.cancer_record_comment'
        db.add_column(u'bcpp_subject_medicaldiagnoses_audit', 'cancer_record_comment',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'MedicalDiagnosesAudit.heart_attack_comment'
        db.add_column(u'bcpp_subject_medicaldiagnoses_audit', 'heart_attack_comment',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'MedicalDiagnosesAudit.tb_record_comment'
        db.add_column(u'bcpp_subject_medicaldiagnoses_audit', 'tb_record_comment',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Changing field 'MedicalDiagnosesAudit.revision'
        db.alter_column(u'bcpp_subject_medicaldiagnoses_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'HivTested.revision'
        db.alter_column(u'bcpp_subject_hivtested', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

    models = {
        'adverse_event.deathcausecategory': {
            'Meta': {'ordering': "['display_index']", 'object_name': 'DeathCauseCategory', 'db_table': "'bhp_adverse_deathcausecategory'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),

            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),

            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'adverse_event.deathcauseinfo': {
            'Meta': {'ordering': "['display_index']", 'object_name': 'DeathCauseInfo', 'db_table': "'bhp_adverse_deathcauseinfo'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),

            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),

            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'adverse_event.deathreasonhospitalized': {
            'Meta': {'ordering': "['display_index']", 'object_name': 'DeathReasonHospitalized', 'db_table': "'bhp_adverse_deathreasonhospitalized'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),

            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'appointment.appointment': {
            'Meta': {'ordering': "['registered_subject', 'appt_datetime']", 'unique_together': "(('registered_subject', 'visit_definition', 'visit_instance'),)", 'object_name': 'Appointment', 'db_table': "'bhp_appointment_appointment'"},
            'appt_close_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'appt_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'appt_reason': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'appt_status': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '25', 'db_index': 'True'}),
            'appt_type': ('django.db.models.fields.CharField', [], {'default': "'clinic'", 'max_length': '20'}),
            'best_appt_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'contact_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'contact_tel': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dashboard_type': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),

            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['registration.RegisteredSubject']"}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'study_site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_variables.StudySite']", 'null': 'True'}),
            'timepoint_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'visit_definition': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['visit_schedule.VisitDefinition']"}),
            'visit_instance': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1', 'null': 'True', 'db_index': 'True', 'blank': 'True'})
        },
        'bcpp_household.household': {
            'Meta': {'ordering': "['-household_identifier']", 'object_name': 'Household'},
            'action': ('django.db.models.fields.CharField', [], {'default': "'unconfirmed'", 'max_length': '25', 'null': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'community': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'enrolled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enumeration_attempts': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'gps_degrees_e': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_degrees_s': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_lat': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'gps_lon': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'gps_minutes_e': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_minutes_s': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_target_lat': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'gps_target_lon': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'hh_int': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'hh_seed': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'unique': 'True', 'null': 'True'}),
            'household_sequence': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'plot': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_household.Plot']", 'null': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'target_radius': ('django.db.models.fields.FloatField', [], {'default': '0.025'}),
            'uploaded_map': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.householdstructure': {
            'Meta': {'object_name': 'HouseholdStructure'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_household.Household']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'member_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'progress': ('django.db.models.fields.CharField', [], {'default': "'Not Started'", 'max_length': '25', 'null': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_survey.Survey']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.plot': {
            'Meta': {'ordering': "['-plot_identifier']", 'unique_together': "(('gps_target_lat', 'gps_target_lon'),)", 'object_name': 'Plot'},
            'access_attempts': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'action': ('django.db.models.fields.CharField', [], {'default': "'unconfirmed'", 'max_length': '25', 'null': 'True'}),
            'bhs': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'community': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'cso_number': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'device_id': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'distance_from_target': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'eligible_members': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gps_degrees_e': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_degrees_s': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_lat': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_lon': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_minutes_e': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_minutes_s': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_target_lat': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_target_lon': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'plot_identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25', 'db_index': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'section': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'selected': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True'}),
            'sub_section': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'target_radius': ('django.db.models.fields.FloatField', [], {'default': '0.025'}),
            'time_of_day': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'time_of_week': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'uploaded_map_16': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'uploaded_map_17': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'uploaded_map_18': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household_member.householdmember': {
            'Meta': {'ordering': "['-created']", 'unique_together': "(('household_structure', 'first_name', 'initials'), ('registered_subject', 'household_structure'))", 'object_name': 'HouseholdMember'},
            'absentee': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'absentee_visit_attempts': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'age_in_years': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_index': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'eligible_member': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'eligible_subject': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'db_index': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_index': 'True'}),
            'hiv_history': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_structure': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_household.HouseholdStructure']", 'null': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '3', 'db_index': 'True'}),
            'internal_identifier': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '36', 'null': 'True'}),
            'member_status': ('django.db.models.fields.CharField', [], {'default': "'NOT_REPORTED'", 'max_length': '25', 'null': 'True', 'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'present_today': ('django.db.models.fields.CharField', [], {'max_length': '3', 'db_index': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['registration.RegisteredSubject']", 'null': 'True'}),
            'relation': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'study_resident': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'target': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_list.circumcisionbenefits': {
            'Meta': {'object_name': 'CircumcisionBenefits'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bcpp_list.diagnoses': {
            'Meta': {'object_name': 'Diagnoses'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bcpp_list.ethnicgroups': {
            'Meta': {'object_name': 'EthnicGroups'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bcpp_list.familyplanning': {
            'Meta': {'object_name': 'FamilyPlanning'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bcpp_list.heartdisease': {
            'Meta': {'object_name': 'HeartDisease'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bcpp_list.livewith': {
            'Meta': {'object_name': 'LiveWith'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bcpp_list.medicalcareaccess': {
            'Meta': {'object_name': 'MedicalCareAccess'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bcpp_list.neighbourhoodproblems': {
            'Meta': {'object_name': 'NeighbourhoodProblems'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bcpp_list.partnerresidency': {
            'Meta': {'object_name': 'PartnerResidency'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bcpp_list.religion': {
            'Meta': {'object_name': 'Religion'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bcpp_list.stiillnesses': {
            'Meta': {'object_name': 'StiIllnesses'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bcpp_subject.accesstocare': {
            'Meta': {'object_name': 'AccessToCare'},
            'access_care': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'access_care_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'convenient_access': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'emergency_access': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'expensive_access': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'local_hiv_care': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'medical_care_access': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bcpp_list.MedicalCareAccess']", 'null': 'True', 'symmetrical': 'False'}),
            'medical_care_access_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'overall_access': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'whenever_access': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'})
        },
        'bcpp_subject.accesstocareaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'AccessToCareAudit', 'db_table': "u'bcpp_subject_accesstocare_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'access_care': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'access_care_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'convenient_access': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'emergency_access': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'expensive_access': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'local_hiv_care': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'medical_care_access_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'overall_access': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_accesstocare'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'whenever_access': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'})
        },
        'bcpp_subject.cancer': {
            'Meta': {'object_name': 'Cancer'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_cancer': ('django.db.models.fields.DateField', [], {}),
            'dx_cancer': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.canceraudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'CancerAudit', 'db_table': "u'bcpp_subject_cancer_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_cancer': ('django.db.models.fields.DateField', [], {}),
            'dx_cancer': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_cancer'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.cd4history': {
            'Meta': {'object_name': 'Cd4History'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'last_cd4_count': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'last_cd4_drawn_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'record_available': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.cd4historyaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'Cd4HistoryAudit', 'db_table': "u'bcpp_subject_cd4history_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'last_cd4_count': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'last_cd4_drawn_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'record_available': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_cd4history'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.ceaenrollmentchecklist': {
            'Meta': {'object_name': 'CeaEnrollmentChecklist'},
            'cd4_count': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'cd4_date': ('django.db.models.fields.DateField', [], {'max_length': '25'}),
            'citizen': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'community_resident': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_signed': ('django.db.models.fields.DateTimeField', [], {'max_length': '25'}),
            'diagnosis_date': ('django.db.models.fields.DateField', [], {'max_length': '3'}),
            'enrollment_reason': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),

            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'legal_marriage': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'marriage_certificate': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'marriage_certificate_no': ('django.db.models.fields.CharField', [], {'max_length': '9', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'opportunistic_illness': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'registered_subject': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['registration.RegisteredSubject']", 'unique': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.ceaenrollmentchecklistaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'CeaEnrollmentChecklistAudit', 'db_table': "u'bcpp_subject_ceaenrollmentchecklist_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'cd4_count': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'cd4_date': ('django.db.models.fields.DateField', [], {'max_length': '25'}),
            'citizen': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'community_resident': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_signed': ('django.db.models.fields.DateTimeField', [], {'max_length': '25'}),
            'diagnosis_date': ('django.db.models.fields.DateField', [], {'max_length': '3'}),
            'enrollment_reason': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'legal_marriage': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'marriage_certificate': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'marriage_certificate_no': ('django.db.models.fields.CharField', [], {'max_length': '9', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'opportunistic_illness': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_ceaenrollmentchecklist'", 'to': "orm['registration.RegisteredSubject']"}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.circumcised': {
            'Meta': {'object_name': 'Circumcised'},
            'circumcised': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'health_benefits_smc': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['bcpp_list.CircumcisionBenefits']", 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'when_circ': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'where_circ': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True'}),
            'where_circ_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'why_circ': ('django.db.models.fields.CharField', [], {'max_length': '55', 'null': 'True'}),
            'why_circ_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'})
        },
        'bcpp_subject.circumcisedaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'CircumcisedAudit', 'db_table': "u'bcpp_subject_circumcised_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'circumcised': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_circumcised'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'when_circ': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'where_circ': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True'}),
            'where_circ_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'why_circ': ('django.db.models.fields.CharField', [], {'max_length': '55', 'null': 'True'}),
            'why_circ_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'})
        },
        'bcpp_subject.circumcision': {
            'Meta': {'object_name': 'Circumcision'},
            'circumcised': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.circumcisionaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'CircumcisionAudit', 'db_table': "u'bcpp_subject_circumcision_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'circumcised': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_circumcision'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.clinicquestionnaire': {
            'Meta': {'object_name': 'ClinicQuestionnaire'},
            'arv_evidence': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'current_hiv_status': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'know_hiv_status': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'on_arv': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.clinicquestionnaireaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'ClinicQuestionnaireAudit', 'db_table': "u'bcpp_subject_clinicquestionnaire_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'arv_evidence': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'current_hiv_status': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'know_hiv_status': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'on_arv': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_clinicquestionnaire'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.communityengagement': {
            'Meta': {'object_name': 'CommunityEngagement'},
            'community_engagement': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'problems_engagement': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bcpp_list.NeighbourhoodProblems']", 'null': 'True', 'symmetrical': 'False'}),
            'problems_engagement_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'solve_engagement': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'vote_engagement': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'})
        },
        'bcpp_subject.communityengagementaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'CommunityEngagementAudit', 'db_table': "u'bcpp_subject_communityengagement_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'community_engagement': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'problems_engagement_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'solve_engagement': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_communityengagement'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'vote_engagement': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'})
        },
        'bcpp_subject.demographics': {
            'Meta': {'object_name': 'Demographics'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'ethnic': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bcpp_list.EthnicGroups']", 'symmetrical': 'False'}),
            'ethnic_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'husband_wives': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'live_with': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bcpp_list.LiveWith']", 'symmetrical': 'False'}),
            'marital_status': ('django.db.models.fields.CharField', [], {'max_length': '55'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'num_wives': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'religion': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bcpp_list.Religion']", 'symmetrical': 'False'}),
            'religion_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.demographicsaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'DemographicsAudit', 'db_table': "u'bcpp_subject_demographics_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'ethnic_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'husband_wives': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'marital_status': ('django.db.models.fields.CharField', [], {'max_length': '55'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'num_wives': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'religion_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_demographics'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.education': {
            'Meta': {'object_name': 'Education'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'education': ('django.db.models.fields.CharField', [], {'max_length': '65'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'job_description': ('django.db.models.fields.CharField', [], {'max_length': '65', 'null': 'True', 'blank': 'True'}),
            'job_type': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'monthly_income': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'reason_unemployed': ('django.db.models.fields.CharField', [], {'max_length': '65', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'working': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        'bcpp_subject.educationaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'EducationAudit', 'db_table': "u'bcpp_subject_education_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'education': ('django.db.models.fields.CharField', [], {'max_length': '65'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'job_description': ('django.db.models.fields.CharField', [], {'max_length': '65', 'null': 'True', 'blank': 'True'}),
            'job_type': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'monthly_income': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'reason_unemployed': ('django.db.models.fields.CharField', [], {'max_length': '65', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_education'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'working': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        'bcpp_subject.futurehivtesting': {
            'Meta': {'object_name': 'FutureHivTesting'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hiv_test_time': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True'}),
            'hiv_test_time_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'hiv_test_week': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True'}),
            'hiv_test_week_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'hiv_test_year': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'hiv_test_year_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'prefer_hivtest': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.futurehivtestingaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'FutureHivTestingAudit', 'db_table': "u'bcpp_subject_futurehivtesting_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hiv_test_time': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True'}),
            'hiv_test_time_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'hiv_test_week': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True'}),
            'hiv_test_week_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'hiv_test_year': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'hiv_test_year_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'prefer_hivtest': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_futurehivtesting'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.grant': {
            'Meta': {'object_name': 'Grant'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'grant_number': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'grant_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'labour_market_wages': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_subject.LabourMarketWages']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'other_grant': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.grantaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'GrantAudit', 'db_table': "u'bcpp_subject_grant_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'grant_number': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'grant_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'labour_market_wages': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_grant'", 'to': "orm['bcpp_subject.LabourMarketWages']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'other_grant': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_grant'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.heartattack': {
            'Meta': {'object_name': 'HeartAttack'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_heart_attack': ('django.db.models.fields.DateField', [], {}),
            'dx_heart_attack': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bcpp_list.HeartDisease']", 'symmetrical': 'False'}),
            'dx_heart_attack_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.heartattackaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HeartAttackAudit', 'db_table': "u'bcpp_subject_heartattack_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_heart_attack': ('django.db.models.fields.DateField', [], {}),
            'dx_heart_attack_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_heartattack'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.hivcareadherence': {
            'Meta': {'object_name': 'HivCareAdherence'},
            'adherence_4_day': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'adherence_4_wk': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'arv_evidence': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'arv_naive': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'arv_stop': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'arv_stop_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'arv_stop_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'ever_recommended_arv': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'first_arv': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'first_positive': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'medical_care': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'no_medical_care': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True', 'blank': 'True'}),
            'no_medical_care_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'on_arv': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'why_no_arv': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'why_no_arv_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'})
        },
        'bcpp_subject.hivcareadherenceaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HivCareAdherenceAudit', 'db_table': "u'bcpp_subject_hivcareadherence_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'adherence_4_day': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'adherence_4_wk': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'arv_evidence': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'arv_naive': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'arv_stop': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'arv_stop_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'arv_stop_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'ever_recommended_arv': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'first_arv': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'first_positive': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'medical_care': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'no_medical_care': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True', 'blank': 'True'}),
            'no_medical_care_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'on_arv': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_hivcareadherence'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'why_no_arv': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'why_no_arv_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'})
        },
        'bcpp_subject.hivhealthcarecosts': {
            'Meta': {'object_name': 'HivHealthCareCosts'},
            'care_regularity': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'doctor_visits': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'hiv_medical_care': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'place_care_received': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'reason_no_care': ('django.db.models.fields.CharField', [], {'max_length': '115', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.hivhealthcarecostsaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HivHealthCareCostsAudit', 'db_table': "u'bcpp_subject_hivhealthcarecosts_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'care_regularity': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'doctor_visits': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'hiv_medical_care': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'place_care_received': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'reason_no_care': ('django.db.models.fields.CharField', [], {'max_length': '115', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_hivhealthcarecosts'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.hivmedicalcare': {
            'Meta': {'object_name': 'HivMedicalCare'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_hiv_care_pos': ('django.db.models.fields.DateField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'last_hiv_care_pos': ('django.db.models.fields.DateField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'lowest_cd4': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.hivmedicalcareaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HivMedicalCareAudit', 'db_table': "u'bcpp_subject_hivmedicalcare_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_hiv_care_pos': ('django.db.models.fields.DateField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'last_hiv_care_pos': ('django.db.models.fields.DateField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'lowest_cd4': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_hivmedicalcare'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.hivresult': {
            'Meta': {'object_name': 'HivResult'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hiv_result': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'hiv_result_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'why_not_tested': ('django.db.models.fields.CharField', [], {'max_length': '65', 'null': 'True', 'blank': 'True'})
        },
        'bcpp_subject.hivresultaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HivResultAudit', 'db_table': "u'bcpp_subject_hivresult_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hiv_result': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'hiv_result_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_hivresult'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'why_not_tested': ('django.db.models.fields.CharField', [], {'max_length': '65', 'null': 'True', 'blank': 'True'})
        },
        'bcpp_subject.hivresultdocumentation': {
            'Meta': {'object_name': 'HivResultDocumentation'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'result_date': ('django.db.models.fields.DateField', [], {}),
            'result_doc_type': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'result_recorded': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.hivresultdocumentationaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HivResultDocumentationAudit', 'db_table': "u'bcpp_subject_hivresultdocumentation_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'result_date': ('django.db.models.fields.DateField', [], {}),
            'result_doc_type': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'result_recorded': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_hivresultdocumentation'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.hivtested': {
            'Meta': {'object_name': 'HivTested'},
            'arvs_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hiv_pills': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'num_hiv_tests': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'where_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '85'}),
            'where_hiv_test_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'why_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '105', 'null': 'True'})
        },
        'bcpp_subject.hivtestedaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HivTestedAudit', 'db_table': "u'bcpp_subject_hivtested_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'arvs_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hiv_pills': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'num_hiv_tests': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_hivtested'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'where_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '85'}),
            'where_hiv_test_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'why_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '105', 'null': 'True'})
        },
        'bcpp_subject.hivtestinghistory': {
            'Meta': {'object_name': 'HivTestingHistory'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'has_record': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'has_tested': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'other_record': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'verbal_hiv_result': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'when_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'})
        },
        'bcpp_subject.hivtestinghistoryaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HivTestingHistoryAudit', 'db_table': "u'bcpp_subject_hivtestinghistory_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'has_record': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'has_tested': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'other_record': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_hivtestinghistory'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'verbal_hiv_result': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'when_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'})
        },
        'bcpp_subject.hivtestreview': {
            'Meta': {'object_name': 'HivTestReview'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hiv_test_date': ('django.db.models.fields.DateField', [], {}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'recorded_hiv_result': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.hivtestreviewaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HivTestReviewAudit', 'db_table': "u'bcpp_subject_hivtestreview_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hiv_test_date': ('django.db.models.fields.DateField', [], {}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'recorded_hiv_result': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_hivtestreview'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.hivuntested': {
            'Meta': {'object_name': 'HivUntested'},
            'arvs_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hiv_pills': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'why_no_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '55', 'null': 'True'})
        },
        'bcpp_subject.hivuntestedaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HivUntestedAudit', 'db_table': "u'bcpp_subject_hivuntested_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'arvs_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hiv_pills': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_hivuntested'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'why_no_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '55', 'null': 'True'})
        },
        'bcpp_subject.hospitaladmission': {
            'Meta': {'object_name': 'HospitalAdmission'},
            'admission_nights': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'facility_hospitalized': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'healthcare_expense': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'hospitalization_costs': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'nights_hospitalized': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'reason_hospitalized': ('django.db.models.fields.CharField', [], {'max_length': '95'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'total_expenses': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'travel_hours': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.hospitaladmissionaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HospitalAdmissionAudit', 'db_table': "u'bcpp_subject_hospitaladmission_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'admission_nights': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'facility_hospitalized': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'healthcare_expense': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'hospitalization_costs': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'nights_hospitalized': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'reason_hospitalized': ('django.db.models.fields.CharField', [], {'max_length': '95'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_hospitaladmission'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'total_expenses': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'travel_hours': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.labourmarketwages': {
            'Meta': {'object_name': 'LabourMarketWages'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'days_inactivite': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'days_not_worked': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'days_worked': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'employed': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'govt_grant': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_income': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'job_description_change': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'monthly_income': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'nights_out': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'occupation': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'occupation_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'other_occupation': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'other_occupation_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'salary_payment': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'weeks_out': ('django.db.models.fields.CharField', [], {'max_length': '17'})
        },
        'bcpp_subject.labourmarketwagesaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'LabourMarketWagesAudit', 'db_table': "u'bcpp_subject_labourmarketwages_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'days_inactivite': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'days_not_worked': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'days_worked': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'employed': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'govt_grant': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_income': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'job_description_change': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'monthly_income': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'nights_out': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'occupation': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'occupation_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'other_occupation': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'other_occupation_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'salary_payment': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_labourmarketwages'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'weeks_out': ('django.db.models.fields.CharField', [], {'max_length': '17'})
        },
        'bcpp_subject.medicaldiagnoses': {
            'Meta': {'object_name': 'MedicalDiagnoses'},
            'cancer_record': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'diagnoses': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bcpp_list.Diagnoses']", 'symmetrical': 'False'}),
            'heart_attack_record': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'cancer_record_comment': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'diagnoses': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bcpp_list.Diagnoses']", 'symmetrical': 'False'}),
            'heart_attack_comment': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'heart_attack_record': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),

            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'tb_record': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'tb_record_comment': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.medicaldiagnosesaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'MedicalDiagnosesAudit', 'db_table': "u'bcpp_subject_medicaldiagnoses_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'cancer_record': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'cancer_record_comment': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'heart_attack_comment': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'heart_attack_record': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_medicaldiagnoses'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'tb_record': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'tb_record_comment': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.monthsrecentpartner': {
            'Meta': {'object_name': 'MonthsRecentPartner'},
            'concurrent': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_condom_freq': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'first_disclose': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'first_exchange': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'first_first_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_first_sex_calc': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'first_haart': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'first_partner_cp': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'first_partner_hiv': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'first_partner_live': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bcpp_list.PartnerResidency']", 'symmetrical': 'False'}),
            'first_relationship': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'first_sex_current': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_sex_freq': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'goods_exchange': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'partner_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'third_last_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'third_last_sex_calc': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.monthsrecentpartneraudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'MonthsRecentPartnerAudit', 'db_table': "u'bcpp_subject_monthsrecentpartner_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'concurrent': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_condom_freq': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'first_disclose': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'first_exchange': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'first_first_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_first_sex_calc': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'first_haart': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'first_partner_cp': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'first_partner_hiv': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'first_relationship': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'first_sex_current': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_sex_freq': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'goods_exchange': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'partner_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_monthsrecentpartner'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'third_last_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'third_last_sex_calc': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.monthssecondpartner': {
            'Meta': {'object_name': 'MonthsSecondPartner'},
            'concurrent': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_condom_freq': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'first_disclose': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'first_exchange': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'first_first_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_first_sex_calc': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'first_haart': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'first_partner_cp': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'first_partner_hiv': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'first_partner_live': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bcpp_list.PartnerResidency']", 'symmetrical': 'False'}),
            'first_relationship': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'first_sex_current': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_sex_freq': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'goods_exchange': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'partner_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'third_last_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'third_last_sex_calc': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.monthssecondpartneraudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'MonthsSecondPartnerAudit', 'db_table': "u'bcpp_subject_monthssecondpartner_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'concurrent': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_condom_freq': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'first_disclose': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'first_exchange': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'first_first_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_first_sex_calc': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'first_haart': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'first_partner_cp': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'first_partner_hiv': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'first_relationship': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'first_sex_current': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_sex_freq': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'goods_exchange': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'partner_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_monthssecondpartner'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'third_last_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'third_last_sex_calc': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.monthsthirdpartner': {
            'Meta': {'object_name': 'MonthsThirdPartner'},
            'concurrent': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_condom_freq': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'first_disclose': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'first_exchange': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'first_first_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_first_sex_calc': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'first_haart': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'first_partner_cp': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'first_partner_hiv': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'first_partner_live': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bcpp_list.PartnerResidency']", 'symmetrical': 'False'}),
            'first_relationship': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'first_sex_current': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_sex_freq': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'goods_exchange': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'partner_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'third_last_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'third_last_sex_calc': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.monthsthirdpartneraudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'MonthsThirdPartnerAudit', 'db_table': "u'bcpp_subject_monthsthirdpartner_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'concurrent': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_condom_freq': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'first_disclose': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'first_exchange': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'first_first_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_first_sex_calc': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'first_haart': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'first_partner_cp': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'first_partner_hiv': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'first_relationship': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'first_sex_current': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_sex_freq': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'goods_exchange': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'partner_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_monthsthirdpartner'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'third_last_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'third_last_sex_calc': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.nonpregnancy': {
            'Meta': {'object_name': 'NonPregnancy'},
            'anc_last_pregnancy': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hiv_last_pregnancy': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'last_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'more_children': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'preg_arv': ('django.db.models.fields.CharField', [], {'max_length': '95', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.nonpregnancyaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'NonPregnancyAudit', 'db_table': "u'bcpp_subject_nonpregnancy_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'anc_last_pregnancy': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hiv_last_pregnancy': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'last_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'more_children': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'preg_arv': ('django.db.models.fields.CharField', [], {'max_length': '95', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_nonpregnancy'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.outpatientcare': {
            'Meta': {'object_name': 'OutpatientCare'},
            'care_reason': ('django.db.models.fields.CharField', [], {'max_length': '95'}),
            'care_reason_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'care_visits': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'cost_cover': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dept_care': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'facility_visited': ('django.db.models.fields.CharField', [], {'max_length': '65'}),
            'govt_health_care': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'outpatient_expense': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'prvt_care': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'specific_clinic': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'trad_care': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'transport_expense': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'travel_time': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'waiting_hours': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'bcpp_subject.outpatientcareaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'OutpatientCareAudit', 'db_table': "u'bcpp_subject_outpatientcare_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'care_reason': ('django.db.models.fields.CharField', [], {'max_length': '95'}),
            'care_reason_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'care_visits': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'cost_cover': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dept_care': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'facility_visited': ('django.db.models.fields.CharField', [], {'max_length': '65'}),
            'govt_health_care': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'outpatient_expense': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'prvt_care': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'specific_clinic': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_outpatientcare'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'trad_care': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'transport_expense': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'travel_time': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'waiting_hours': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'bcpp_subject.pima': {
            'Meta': {'object_name': 'Pima'},
            'cd4_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'cd4_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'pima_id': ('django.db.models.fields.CharField', [], {'max_length': '9', 'null': 'True', 'blank': 'True'}),
            'pima_today': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'pima_today_other': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.pimaaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'PimaAudit', 'db_table': "u'bcpp_subject_pima_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'cd4_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'cd4_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'pima_id': ('django.db.models.fields.CharField', [], {'max_length': '9', 'null': 'True', 'blank': 'True'}),
            'pima_today': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'pima_today_other': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_pima'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.positiveparticipant': {
            'Meta': {'object_name': 'PositiveParticipant'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'enacted_jobs_tigma': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'enacted_respect_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'enacted_talk_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'family_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'friend_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'internalize_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'internalized_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.positiveparticipantaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'PositiveParticipantAudit', 'db_table': "u'bcpp_subject_positiveparticipant_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'enacted_jobs_tigma': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'enacted_respect_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'enacted_talk_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'family_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'friend_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'internalize_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'internalized_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_positiveparticipant'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.pregnancy': {
            'Meta': {'object_name': 'Pregnancy'},
            'anc_last_pregnancy': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'anc_reg': ('django.db.models.fields.CharField', [], {'max_length': '55', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hiv_last_pregnancy': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'last_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'lnmp': ('django.db.models.fields.DateField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'preg_arv': ('django.db.models.fields.CharField', [], {'max_length': '95', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.pregnancyaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'PregnancyAudit', 'db_table': "u'bcpp_subject_pregnancy_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'anc_last_pregnancy': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'anc_reg': ('django.db.models.fields.CharField', [], {'max_length': '55', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hiv_last_pregnancy': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'last_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'lnmp': ('django.db.models.fields.DateField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'preg_arv': ('django.db.models.fields.CharField', [], {'max_length': '95', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_pregnancy'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.qualityoflife': {
            'Meta': {'object_name': 'QualityOfLife'},
            'activities': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'anxiety': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'health_today': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'mobility': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'pain': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'self_care': ('django.db.models.fields.CharField', [], {'max_length': '65'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.qualityoflifeaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'QualityOfLifeAudit', 'db_table': "u'bcpp_subject_qualityoflife_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'activities': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'anxiety': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'health_today': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'mobility': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'pain': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'self_care': ('django.db.models.fields.CharField', [], {'max_length': '65'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_qualityoflife'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.reproductivehealth': {
            'Meta': {'object_name': 'ReproductiveHealth'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'currently_pregnant': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'family_planning': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['bcpp_list.FamilyPlanning']", 'null': 'True', 'blank': 'True'}),
            'family_planning_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'menopause': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'number_children': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.reproductivehealthaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'ReproductiveHealthAudit', 'db_table': "u'bcpp_subject_reproductivehealth_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'currently_pregnant': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'family_planning_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'menopause': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'number_children': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_reproductivehealth'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.residencymobility': {
            'Meta': {'object_name': 'ResidencyMobility'},
            'cattle_postlands': ('django.db.models.fields.CharField', [], {'default': "'N/A'", 'max_length': '25'}),
            'cattle_postlands_other': ('django.db.models.fields.CharField', [], {'max_length': '65', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'intend_residency': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'length_residence': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'nights_away': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'permanent_resident': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.residencymobilityaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'ResidencyMobilityAudit', 'db_table': "u'bcpp_subject_residencymobility_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'cattle_postlands': ('django.db.models.fields.CharField', [], {'default': "'N/A'", 'max_length': '25'}),
            'cattle_postlands_other': ('django.db.models.fields.CharField', [], {'max_length': '65', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'intend_residency': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'length_residence': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'nights_away': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'permanent_resident': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_residencymobility'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.resourceutilization': {
            'Meta': {'object_name': 'ResourceUtilization'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hospitalized': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'medical_cover': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'money_spent': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'out_patient': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.resourceutilizationaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'ResourceUtilizationAudit', 'db_table': "u'bcpp_subject_resourceutilization_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hospitalized': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'medical_cover': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'money_spent': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'out_patient': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_resourceutilization'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.sexualbehaviour': {
            'Meta': {'object_name': 'SexualBehaviour'},
            'alcohol_sex': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'condom': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'ever_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_sex': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'last_year_partners': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'lifetime_sex_partners': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'more_sex': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.sexualbehaviouraudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'SexualBehaviourAudit', 'db_table': "u'bcpp_subject_sexualbehaviour_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'alcohol_sex': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'condom': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'ever_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_sex': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'last_year_partners': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'lifetime_sex_partners': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'more_sex': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_sexualbehaviour'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.sti': {
            'Meta': {'object_name': 'Sti'},
            'comments': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'diarrhoea_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'herpes_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'pcp_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'pneumonia_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'sti_dx': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bcpp_list.StiIllnesses']", 'symmetrical': 'False'}),
            'sti_dx_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'wasting_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'yeast_infection_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        'bcpp_subject.stiaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'StiAudit', 'db_table': "u'bcpp_subject_sti_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'diarrhoea_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'herpes_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'pcp_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'pneumonia_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'sti_dx_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_sti'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'wasting_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'yeast_infection_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        'bcpp_subject.stigma': {
            'Meta': {'object_name': 'Stigma'},
            'anticipate_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'children_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'enacted_shame_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'saliva_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'teacher_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.stigmaaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'StigmaAudit', 'db_table': "u'bcpp_subject_stigma_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'anticipate_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'children_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'enacted_shame_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'saliva_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_stigma'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'teacher_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.stigmaopinion': {
            'Meta': {'object_name': 'StigmaOpinion'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'enacted_family_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'enacted_phyical_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'enacted_verbal_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'fear_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'gossip_community_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'respect_community_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'test_community_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.stigmaopinionaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'StigmaOpinionAudit', 'db_table': "u'bcpp_subject_stigmaopinion_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'enacted_family_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'enacted_phyical_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'enacted_verbal_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'fear_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'gossip_community_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'respect_community_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_stigmaopinion'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'test_community_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectconsent': {
            'Meta': {'unique_together': "(('subject_identifier', 'survey'),)", 'object_name': 'SubjectConsent'},
            'assessment_score': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'community': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'confirm_identity': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'consent_copy': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'consent_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'consent_reviewed': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'consent_signature': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'consent_version_on_entry': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'consent_version_recent': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'guardian_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_household_member.HouseholdMember']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'identity': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '78L'}),
            'identity_type': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'is_dob_estimated': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'is_incarcerated': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '3'}),
            'is_literate': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '3'}),
            'is_minor': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '10', 'null': 'True'}),
            'is_signed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_verified_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'not specified'", 'max_length': '25'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'may_store_samples': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['registration.RegisteredSubject']", 'null': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'study_questions': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'study_site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_variables.StudySite']", 'null': 'True'}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'subject_identifier_as_pk': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'subject_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_survey.Survey']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'witness_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'})
        },
        'bcpp_subject.subjectconsentaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'SubjectConsentAudit', 'db_table': "u'bcpp_subject_subjectconsent_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'assessment_score': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'community': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'confirm_identity': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'consent_copy': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'consent_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'consent_reviewed': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'consent_signature': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'consent_version_on_entry': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'consent_version_recent': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'guardian_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectconsent'", 'to': "orm['bcpp_household_member.HouseholdMember']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'identity': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'identity_type': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'is_dob_estimated': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'is_incarcerated': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '3'}),
            'is_literate': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '3'}),
            'is_minor': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '10', 'null': 'True'}),
            'is_signed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_verified_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'not specified'", 'max_length': '25'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'may_store_samples': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectconsent'", 'null': 'True', 'to': "orm['registration.RegisteredSubject']"}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'study_questions': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'study_site': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectconsent'", 'null': 'True', 'to': "orm['bhp_variables.StudySite']"}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'subject_identifier_as_pk': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'subject_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectconsent'", 'to': "orm['bcpp_survey.Survey']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'witness_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'})
        },
        'bcpp_subject.subjectconsenthistory': {
            'Meta': {'object_name': 'SubjectConsentHistory'},
            'consent_app_label': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'consent_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'consent_model_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'consent_pk': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_household_member.HouseholdMember']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['registration.RegisteredSubject']"}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_survey.Survey']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectconsentrbd': {
            'Meta': {'unique_together': "(('subject_identifier', 'survey'),)", 'object_name': 'SubjectConsentRbd'},
            'assessment_score': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'community': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'confirm_identity': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'consent_copy': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'consent_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'consent_reviewed': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'consent_signature': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'consent_version_on_entry': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'consent_version_recent': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'guardian_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_household_member.HouseholdMember']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'identity': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '78L'}),
            'identity_type': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'is_dob_estimated': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'is_incarcerated': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '3'}),
            'is_literate': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '3'}),
            'is_minor': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '10', 'null': 'True'}),
            'is_signed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_verified_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'not specified'", 'max_length': '25'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'may_store_samples': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['registration.RegisteredSubject']", 'null': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'study_questions': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'study_site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_variables.StudySite']", 'null': 'True'}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'subject_identifier_as_pk': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'subject_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_survey.Survey']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'witness_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'})
        },
        'bcpp_subject.subjectconsentrbdaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'SubjectConsentRbdAudit', 'db_table': "u'bcpp_subject_subjectconsentrbd_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'assessment_score': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'community': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'confirm_identity': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'consent_copy': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'consent_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'consent_reviewed': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'consent_signature': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'consent_version_on_entry': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'consent_version_recent': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'guardian_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectconsentrbd'", 'to': "orm['bcpp_household_member.HouseholdMember']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'identity': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'identity_type': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'is_dob_estimated': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'is_incarcerated': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '3'}),
            'is_literate': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '3'}),
            'is_minor': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '10', 'null': 'True'}),
            'is_signed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_verified_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'not specified'", 'max_length': '25'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'may_store_samples': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectconsentrbd'", 'null': 'True', 'to': "orm['registration.RegisteredSubject']"}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'study_questions': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'study_site': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectconsentrbd'", 'null': 'True', 'to': "orm['bhp_variables.StudySite']"}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'subject_identifier_as_pk': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'subject_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectconsentrbd'", 'to': "orm['bcpp_survey.Survey']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'witness_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'})
        },
        'bcpp_subject.subjectdeath': {
            'Meta': {'object_name': 'SubjectDeath'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'days_decedent_hospitalized': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'days_hospitalized': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'death_cause': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'death_cause_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['adverse_event.DeathCauseCategory']"}),
            'death_cause_info': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['adverse_event.DeathCauseInfo']"}),
            'death_cause_info_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'death_cause_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'death_date': ('django.db.models.fields.DateField', [], {}),
            'death_reason_hospitalized': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['adverse_event.DeathReasonHospitalized']", 'null': 'True', 'blank': 'True'}),
            'death_year': ('django.db.models.fields.DateField', [], {}),
            'decedent_haart': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'decedent_haart_start': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'decedent_hospitalized': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'decendent_death_age': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'doctor_evaluation': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'document_community': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'document_community_other': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'document_hiv': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'hospital_death': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'hospital_visits': ('django.db.models.fields.IntegerField', [], {}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'participant_hospitalized': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'registered_subject': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['registration.RegisteredSubject']", 'unique': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'sufficient_records': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectdeathaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'SubjectDeathAudit', 'db_table': "u'bcpp_subject_subjectdeath_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'days_decedent_hospitalized': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'days_hospitalized': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'death_cause': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'death_cause_category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectdeath'", 'to': "orm['adverse_event.DeathCauseCategory']"}),
            'death_cause_info': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectdeath'", 'to': "orm['adverse_event.DeathCauseInfo']"}),
            'death_cause_info_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'death_cause_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'death_date': ('django.db.models.fields.DateField', [], {}),
            'death_reason_hospitalized': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'_audit_subjectdeath'", 'null': 'True', 'to': "orm['adverse_event.DeathReasonHospitalized']"}),
            'death_year': ('django.db.models.fields.DateField', [], {}),
            'decedent_haart': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'decedent_haart_start': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'decedent_hospitalized': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'decendent_death_age': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'doctor_evaluation': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'document_community': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'document_community_other': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'document_hiv': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'hospital_death': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'hospital_visits': ('django.db.models.fields.IntegerField', [], {}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'participant_hospitalized': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectdeath'", 'to': "orm['registration.RegisteredSubject']"}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'sufficient_records': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectlocator': {
            'Meta': {'object_name': 'SubjectLocator'},
            'alt_contact_cell': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'alt_contact_cell_number': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'alt_contact_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'alt_contact_rel': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'alt_contact_tel': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'contact_cell': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'contact_physical_address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'contact_rel': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_signed': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'has_alt_contact': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'home_visit_permission': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'mail_address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'may_call_work': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'may_contact_someone': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'may_follow_up': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'may_sms_follow_up': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'other_alt_contact_cell': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'physical_address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['registration.RegisteredSubject']", 'unique': 'True', 'null': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_cell': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'subject_cell_alt': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'subject_phone': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'subject_phone_alt': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'null': 'True'}),
            'subject_work_phone': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'subject_work_place': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectlocatoraudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'SubjectLocatorAudit', 'db_table': "u'bcpp_subject_subjectlocator_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'alt_contact_cell': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'alt_contact_cell_number': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'alt_contact_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'alt_contact_rel': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'alt_contact_tel': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'contact_cell': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'contact_physical_address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'contact_rel': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_signed': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'has_alt_contact': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'home_visit_permission': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'mail_address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'may_call_work': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'may_contact_someone': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'may_follow_up': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'may_sms_follow_up': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'other_alt_contact_cell': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'physical_address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectlocator'", 'null': 'True', 'to': "orm['registration.RegisteredSubject']"}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_cell': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'subject_cell_alt': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'subject_phone': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'subject_phone_alt': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectlocator'", 'null': 'True', 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'subject_work_phone': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'subject_work_place': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectoffstudy': {
            'Meta': {'object_name': 'SubjectOffStudy'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'has_scheduled_data': ('django.db.models.fields.CharField', [], {'default': "'Yes'", 'max_length': '10'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'offstudy_date': ('django.db.models.fields.DateField', [], {}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'reason_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['registration.RegisteredSubject']", 'unique': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectoffstudyaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'SubjectOffStudyAudit', 'db_table': "u'bcpp_subject_subjectoffstudy_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'has_scheduled_data': ('django.db.models.fields.CharField', [], {'default': "'Yes'", 'max_length': '10'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'offstudy_date': ('django.db.models.fields.DateField', [], {}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'reason_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectoffstudy'", 'to': "orm['registration.RegisteredSubject']"}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectreferral': {
            'Meta': {'object_name': 'SubjectReferral'},
            'cd4_result': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2'}),
            'cd4_result_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'circumcised': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'citizen': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'export_uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'exported': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'exported_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'hiv_result': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'hiv_result_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'in_clinic_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'intend_residency': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'last_cd4_result': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'last_cd4_test_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_hiv_result': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'last_hiv_test_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'new_pos': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'on_art': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'permanent_resident': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'pregnant': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'referral_appt_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'referral_clinic': ('django.db.models.fields.CharField', [], {'default': "'otse'", 'max_length': '50'}),
            'referral_clinic_other': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'referral_code': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'referred_from_bhs': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'urgent_referral': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'vl_sample_datetime_drawn': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'vl_sample_drawn': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        'bcpp_subject.subjectreferralaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'SubjectReferralAudit', 'db_table': "u'bcpp_subject_subjectreferral_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'cd4_result': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2'}),
            'cd4_result_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'circumcised': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'citizen': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'export_uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'exported': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'exported_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'hiv_result': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'hiv_result_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'in_clinic_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'intend_residency': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'last_cd4_result': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'last_cd4_test_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_hiv_result': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'last_hiv_test_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'new_pos': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'on_art': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'permanent_resident': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'pregnant': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'referral_appt_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'referral_clinic': ('django.db.models.fields.CharField', [], {'default': "'otse'", 'max_length': '50'}),
            'referral_clinic_other': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'referral_code': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'referred_from_bhs': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectreferral'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'urgent_referral': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'vl_sample_datetime_drawn': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'vl_sample_drawn': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        'bcpp_subject.subjectvisit': {
            'Meta': {'object_name': 'SubjectVisit'},
            'appointment': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['appointment.Appointment']", 'unique': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_household_member.HouseholdMember']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'info_source': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'info_source_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'reason_missed': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'reason_unscheduled': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectvisitaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'SubjectVisitAudit', 'db_table': "u'bcpp_subject_subjectvisit_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'appointment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectvisit'", 'to': "orm['appointment.Appointment']"}),
            'comments': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectvisit'", 'to': "orm['bcpp_household_member.HouseholdMember']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'info_source': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'info_source_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'reason_missed': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'reason_unscheduled': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.substanceuse': {
            'Meta': {'object_name': 'SubstanceUse'},
            'alcohol': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'smoke': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.substanceuseaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'SubstanceUseAudit', 'db_table': "u'bcpp_subject_substanceuse_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'alcohol': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'smoke': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_substanceuse'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.tubercolosis': {
            'Meta': {'object_name': 'Tubercolosis'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_tb': ('django.db.models.fields.DateField', [], {}),
            'dx_tb': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.tubercolosisaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'TubercolosisAudit', 'db_table': "u'bcpp_subject_tubercolosis_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_tb': ('django.db.models.fields.DateField', [], {}),
            'dx_tb': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_tubercolosis'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.uncircumcised': {
            'Meta': {'object_name': 'Uncircumcised'},
            'aware_free': ('django.db.models.fields.CharField', [], {'max_length': '85', 'null': 'True', 'blank': 'True'}),
            'circumcised': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'future_circ': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'future_reasons_smc': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True'}),
            'health_benefits_smc': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['bcpp_list.CircumcisionBenefits']", 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'reason_circ': ('django.db.models.fields.CharField', [], {'max_length': '65', 'null': 'True'}),
            'reason_circ_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'service_facilities': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.uncircumcisedaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'UncircumcisedAudit', 'db_table': "u'bcpp_subject_uncircumcised_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'aware_free': ('django.db.models.fields.CharField', [], {'max_length': '85', 'null': 'True', 'blank': 'True'}),
            'circumcised': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'future_circ': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'future_reasons_smc': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'reason_circ': ('django.db.models.fields.CharField', [], {'max_length': '65', 'null': 'True'}),
            'reason_circ_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 7, 0, 0)'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'service_facilities': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_uncircumcised'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_survey.survey': {
            'Meta': {'ordering': "['survey_name']", 'object_name': 'Survey'},
            'chronological_order': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'datetime_end': ('django.db.models.fields.DateTimeField', [], {}),
            'datetime_start': ('django.db.models.fields.DateTimeField', [], {}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'survey_description': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'survey_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15', 'db_index': 'True'}),
            'survey_slug': ('django.db.models.fields.SlugField', [], {'max_length': '40'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bhp_content_type_map.contenttypemap': {
            'Meta': {'ordering': "['name']", 'unique_together': "(['app_label', 'model'],)", 'object_name': 'ContentTypeMap'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'module_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bhp_variables.studysite': {
            'Meta': {'ordering': "['site_code']", 'unique_together': "[('site_code', 'site_name')]", 'object_name': 'StudySite'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'site_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4'}),
            'site_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '35'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'registration.registeredsubject': {
            'Meta': {'ordering': "['subject_identifier']", 'unique_together': "(('first_name', 'dob', 'initials'),)", 'object_name': 'RegisteredSubject', 'db_table': "'bhp_registration_registeredsubject'"},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'hiv_status': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'identity': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'identity_type': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'is_dob_estimated': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'may_store_samples': ('django.db.models.fields.CharField', [], {'default': "'?'", 'max_length': '3'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'randomization_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'registration_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'registration_identifier': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'registration_status': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'relative_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'salt': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'screening_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'sid': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'study_site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_variables.StudySite']", 'null': 'True', 'blank': 'True'}),
            'subject_consent_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'subject_identifier_as_pk': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'subject_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'survival_status': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'visit_schedule.membershipform': {
            'Meta': {'object_name': 'MembershipForm', 'db_table': "'bhp_visit_membershipform'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'default': "'subject'", 'max_length': '25', 'unique': 'True', 'null': 'True'}),
            'content_type_map': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'+'", 'unique': 'True', 'to': "orm['bhp_content_type_map.ContentTypeMap']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'visit_schedule.schedulegroup': {
            'Meta': {'ordering': "['group_name']", 'object_name': 'ScheduleGroup', 'db_table': "'bhp_visit_schedulegroup'"},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'group_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'}),
            'grouping_key': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'membership_form': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['visit_schedule.MembershipForm']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'visit_schedule.visitdefinition': {
            'Meta': {'ordering': "['code', 'time_point']", 'object_name': 'VisitDefinition', 'db_table': "'bhp_visit_visitdefinition'"},
            'base_interval': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'base_interval_unit': ('django.db.models.fields.CharField', [], {'default': "'D'", 'max_length': '10'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '6', 'db_index': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'grouping': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'instruction': ('django.db.models.fields.TextField', [], {'max_length': '255', 'blank': 'True'}),
            'lower_window': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'lower_window_unit': ('django.db.models.fields.CharField', [], {'default': "'D'", 'max_length': '10'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'schedule_group': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['visit_schedule.ScheduleGroup']", 'null': 'True', 'blank': 'True'}),
            'time_point': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '35', 'db_index': 'True'}),
            'upper_window': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'upper_window_unit': ('django.db.models.fields.CharField', [], {'default': "'D'", 'max_length': '10'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'visit_tracking_content_type_map': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_content_type_map.ContentTypeMap']", 'null': 'True'})
        }
    }

    complete_apps = ['bcpp_subject']