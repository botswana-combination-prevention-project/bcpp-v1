from . import (SubjectOffStudy, SubjectVisit, HicEnrollment, SubjectConsentHistory, SubjectConsent, SubjectLocator,
               QualityOfLife, ResourceUtilization, OutpatientCare, HospitalAdmission,
               HivHealthCareCosts, LabourMarketWages, Grant, CeaEnrollmentChecklist, ResidencyMobility,
               Demographics, CommunityEngagement, Education, HivTestingHistory, HivTestReview,
               HivTested, HivUntested, SexualBehaviour, MonthsRecentPartner, MonthsSecondPartner,
               MonthsThirdPartner, HivCareAdherence, HivMedicalCare, Circumcision, Circumcised,
               Uncircumcised, ReproductiveHealth, MedicalDiagnoses, HeartAttack, Cancer, Tubercolosis,
               Sti, SubstanceUse, Stigma, StigmaOpinion, PositiveParticipant, AccessToCare,
               HivResult, Pregnancy, NonPregnancy, HivResultDocumentation, Pima, Cd4History,
               ClinicQuestionnaire, TbSymptoms, SubjectReferral, Participation, RbdDemographics)


class SubjectOffStudyReview(SubjectOffStudy):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class SubjectVisitReview(SubjectVisit):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class HicEnrollmentReview(HicEnrollment):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class SubjectConsentHistoryReview(SubjectConsentHistory):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class SubjectConsentReview(SubjectConsent):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class SubjectLocatorReview(SubjectLocator):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class QualityOfLifeReview(QualityOfLife):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class ResourceUtilizationReview(ResourceUtilization):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class OutpatientCareReview(OutpatientCare):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class HospitalAdmissionReview(HospitalAdmission):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class HivHealthCareCostsReview(HivHealthCareCosts):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class LabourMarketWagesReview(LabourMarketWages):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class GrantReview(Grant):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class CeaEnrollmentChecklistReview(CeaEnrollmentChecklist):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class ResidencyMobilityReview(ResidencyMobility):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class DemographicsReview(Demographics):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class CommunityEngagementReview(CommunityEngagement):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class EducationReview(Education):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class HivTestingHistoryReview(HivTestingHistory):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class HivTestReviewReview(HivTestReview):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class HivTestedReview(HivTested):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class HivUntestedReview(HivUntested):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class SexualBehaviourReview(SexualBehaviour):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class MonthsRecentPartnerReview(MonthsRecentPartner):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class MonthsSecondPartnerReview(MonthsSecondPartner):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class MonthsThirdPartnerReview(MonthsThirdPartner):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class HivCareAdherenceReview(HivCareAdherence):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class HivMedicalCareReview(HivMedicalCare):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class CircumcisionReview(Circumcision):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class CircumcisedReview(Circumcised):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class UncircumcisedReview(Uncircumcised):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class ReproductiveHealthReview(ReproductiveHealth):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class MedicalDiagnosesReview(MedicalDiagnoses):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class HeartAttackReview(HeartAttack):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class CancerReview(Cancer):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class TubercolosisReview(Tubercolosis):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class StiReview(Sti):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class SubstanceUseReview(SubstanceUse):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class StigmaReview(Stigma):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class StigmaOpinionReview(StigmaOpinion):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class PositiveParticipantReview(PositiveParticipant):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class AccessToCareReview(AccessToCare):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class HivResultReview(HivResult):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class PregnancyReview(Pregnancy):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class NonPregnancyReview(NonPregnancy):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class HivResultDocumentationReview(HivResultDocumentation):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class PimaReview(Pima):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class Cd4HistoryReview(Cd4History):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class ClinicQuestionnaireReview(ClinicQuestionnaire):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class TbSymptomsReview(TbSymptoms):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class SubjectReferralReview(SubjectReferral):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class ParticipationReview(Participation):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True


class RbdDemographicsReview(RbdDemographics):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject_review'
        proxy = True
