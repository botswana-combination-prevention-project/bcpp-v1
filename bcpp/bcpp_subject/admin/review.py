from django.contrib import admin

from .subject_visit_model_admin import SubjectVisitModelAdmin

from ..models import (SubjectReferralReview, HicEnrollmentReview, SubjectLocatorReview, QualityOfLifeReview,
                      ResourceUtilizationReview, OutpatientCareReview, HospitalAdmissionReview,
                      HivHealthCareCostsReview, LabourMarketWagesReview, GrantReview,
                      ResidencyMobilityReview, DemographicsReview, CommunityEngagementReview,
                      EducationReview, HivTestingHistoryReview, HivTestReviewReview, HivTestedReview,
                      HivUntestedReview, SexualBehaviourReview, MonthsRecentPartnerReview,
                      MonthsSecondPartnerReview, MonthsThirdPartnerReview, HivCareAdherenceReview,
                      HivMedicalCareReview, CircumcisionReview, CircumcisedReview, UncircumcisedReview,
                      ReproductiveHealthReview, MedicalDiagnosesReview, HeartAttackReview,
                      CancerReview, TubercolosisReview, StiReview, SubstanceUseReview, StigmaReview,
                      StigmaOpinionReview, PositiveParticipantReview, AccessToCareReview,
                      HivResultReview, PregnancyReview, NonPregnancyReview, HivResultDocumentationReview,
                      PimaReview, Cd4HistoryReview, ClinicQuestionnaireReview, TbSymptomsReview,
                      ParticipationReview, RbdDemographicsReview)


class SubjectReferralReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(SubjectReferralReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in SubjectReferralReview._meta.fields]
admin.site.register(SubjectReferralReview, SubjectReferralReviewAdmin)


class HicEnrollmentReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(HicEnrollmentReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in HicEnrollmentReview._meta.fields]

admin.site.register(HicEnrollmentReview, HicEnrollmentReviewAdmin)


class SubjectLocatorReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(SubjectLocatorReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in SubjectLocatorReview._meta.fields]

admin.site.register(SubjectLocatorReview, SubjectLocatorReviewAdmin)


class QualityOfLifeReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(QualityOfLifeReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in QualityOfLifeReview._meta.fields]

admin.site.register(QualityOfLifeReview, QualityOfLifeReviewAdmin)


class ResourceUtilizationReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(ResourceUtilizationReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in ResourceUtilizationReview._meta.fields]

admin.site.register(ResourceUtilizationReview, ResourceUtilizationReviewAdmin)


class OutpatientCareReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(OutpatientCareReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in OutpatientCareReview._meta.fields]

admin.site.register(OutpatientCareReview, OutpatientCareReviewAdmin)


class HospitalAdmissionReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(HospitalAdmissionReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in HospitalAdmissionReview._meta.fields]

admin.site.register(HospitalAdmissionReview, HospitalAdmissionReviewAdmin)


class HivHealthCareCostsReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(HivHealthCareCostsReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in HivHealthCareCostsReview._meta.fields]

admin.site.register(HivHealthCareCostsReview, HivHealthCareCostsReviewAdmin)


class LabourMarketWagesReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(LabourMarketWagesReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in LabourMarketWagesReview._meta.fields]

admin.site.register(LabourMarketWagesReview, LabourMarketWagesReviewAdmin)


class GrantReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(GrantReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in GrantReview._meta.fields]

admin.site.register(GrantReview, GrantReviewAdmin)


# class CeaEnrollmentChecklistReviewAdmin(SubjectVisitModelAdmin):
#     def __init__(self, *args, **kwargs):
#         super(CeaEnrollmentChecklistReviewAdmin, self).__init__(*args, **kwargs)
#         self.readonly_fields = [field.name for field in CeaEnrollmentChecklistReview._meta.fields]
#
# admin.site.register(CeaEnrollmentChecklistReview, CeaEnrollmentChecklistReviewAdmin)


class ResidencyMobilityReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(ResidencyMobilityReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in ResidencyMobilityReview._meta.fields]

admin.site.register(ResidencyMobilityReview, ResidencyMobilityReviewAdmin)


class DemographicsReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(DemographicsReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in DemographicsReview._meta.fields]

admin.site.register(DemographicsReview, DemographicsReviewAdmin)


class CommunityEngagementReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(CommunityEngagementReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in CommunityEngagementReview._meta.fields]

admin.site.register(CommunityEngagementReview, CommunityEngagementReviewAdmin)


class EducationReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(EducationReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in EducationReview._meta.fields]

admin.site.register(EducationReview, EducationReviewAdmin)


class HivTestingHistoryReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(HivTestingHistoryReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in HivTestingHistoryReview._meta.fields]

admin.site.register(HivTestingHistoryReview, HivTestingHistoryReviewAdmin)


class HivTestReviewReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(HivTestReviewReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in HivTestReviewReview._meta.fields]

admin.site.register(HivTestReviewReview, HivTestReviewReviewAdmin)


class HivTestedReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(HivTestedReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in HivTestedReview._meta.fields]

admin.site.register(HivTestedReview, HivTestedReviewAdmin)


class HivUntestedReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(HivUntestedReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in HivUntestedReview._meta.fields]

admin.site.register(HivUntestedReview, HivUntestedReviewAdmin)


class SexualBehaviourReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(SexualBehaviourReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in SexualBehaviourReview._meta.fields]

admin.site.register(SexualBehaviourReview, SexualBehaviourReviewAdmin)


class MonthsRecentPartnerReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(MonthsRecentPartnerReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in MonthsRecentPartnerReview._meta.fields]

admin.site.register(MonthsRecentPartnerReview, MonthsRecentPartnerReviewAdmin)


class MonthsSecondPartnerReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(MonthsSecondPartnerReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in MonthsSecondPartnerReview._meta.fields]

admin.site.register(MonthsSecondPartnerReview, MonthsSecondPartnerReviewAdmin)


class MonthsThirdPartnerReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(MonthsThirdPartnerReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in MonthsThirdPartnerReview._meta.fields]

admin.site.register(MonthsThirdPartnerReview, MonthsThirdPartnerReviewAdmin)


class HivCareAdherenceReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(HivCareAdherenceReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in HivCareAdherenceReview._meta.fields]

admin.site.register(HivCareAdherenceReview, HivCareAdherenceReviewAdmin)


class HivMedicalCareReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(HivMedicalCareReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in HivMedicalCareReview._meta.fields]

admin.site.register(HivMedicalCareReview, HivMedicalCareReviewAdmin)


class CircumcisionReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(CircumcisionReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in CircumcisionReview._meta.fields]

admin.site.register(CircumcisionReview, CircumcisionReviewAdmin)


class CircumcisedReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(CircumcisedReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in CircumcisedReview._meta.fields]

admin.site.register(CircumcisedReview, CircumcisedReviewAdmin)


class UncircumcisedReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(UncircumcisedReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in UncircumcisedReview._meta.fields]

admin.site.register(UncircumcisedReview, UncircumcisedReviewAdmin)


class ReproductiveHealthReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(ReproductiveHealthReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in ReproductiveHealthReview._meta.fields]

admin.site.register(ReproductiveHealthReview, ReproductiveHealthReviewAdmin)


class MedicalDiagnosesReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(MedicalDiagnosesReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in MedicalDiagnosesReview._meta.fields]

admin.site.register(MedicalDiagnosesReview, MedicalDiagnosesReviewAdmin)


class HeartAttackReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(HeartAttackReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in HeartAttackReview._meta.fields]

admin.site.register(HeartAttackReview, HeartAttackReviewAdmin)


class CancerReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(CancerReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in CancerReview._meta.fields]

admin.site.register(CancerReview, CancerReviewAdmin)


class TubercolosisReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(TubercolosisReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in TubercolosisReview._meta.fields]

admin.site.register(TubercolosisReview, TubercolosisReviewAdmin)


class StiReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(StiReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in StiReview._meta.fields]

admin.site.register(StiReview, StiReviewAdmin)


class SubstanceUseReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(SubstanceUseReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in SubstanceUseReview._meta.fields]

admin.site.register(SubstanceUseReview, SubstanceUseReviewAdmin)


class StigmaReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(StigmaReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in StigmaReview._meta.fields]

admin.site.register(StigmaReview, StigmaReviewAdmin)


class StigmaOpinionReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(StigmaOpinionReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in StigmaOpinionReview._meta.fields]

admin.site.register(StigmaOpinionReview, StigmaOpinionReviewAdmin)


class PositiveParticipantReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(PositiveParticipantReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in PositiveParticipantReview._meta.fields]

admin.site.register(PositiveParticipantReview, PositiveParticipantReviewAdmin)


class AccessToCareReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(AccessToCareReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in AccessToCareReview._meta.fields]

admin.site.register(AccessToCareReview, AccessToCareReviewAdmin)


class HivResultReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(HivResultReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in HivResultReview._meta.fields]

admin.site.register(HivResultReview, HivResultReviewAdmin)


class PregnancyReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(PregnancyReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in PregnancyReview._meta.fields]

admin.site.register(PregnancyReview, PregnancyReviewAdmin)


class NonPregnancyReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(NonPregnancyReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in NonPregnancyReview._meta.fields]

admin.site.register(NonPregnancyReview, NonPregnancyReviewAdmin)


class HivResultDocumentationReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(HivResultDocumentationReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in HivResultDocumentationReview._meta.fields]

admin.site.register(HivResultDocumentationReview, HivResultDocumentationReviewAdmin)


class PimaReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(PimaReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in PimaReview._meta.fields]

admin.site.register(PimaReview, PimaReviewAdmin)


class Cd4HistoryReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(Cd4HistoryReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in Cd4HistoryReview._meta.fields]

admin.site.register(Cd4HistoryReview, Cd4HistoryReviewAdmin)


class ClinicQuestionnaireReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(ClinicQuestionnaireReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in ClinicQuestionnaireReview._meta.fields]

admin.site.register(ClinicQuestionnaireReview, ClinicQuestionnaireReviewAdmin)


class TbSymptomsReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(TbSymptomsReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in TbSymptomsReview._meta.fields]

admin.site.register(TbSymptomsReview, TbSymptomsReviewAdmin)


class ParticipationReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(ParticipationReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in ParticipationReview._meta.fields]

admin.site.register(ParticipationReview, ParticipationReviewAdmin)


class RbdDemographicsReviewAdmin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super(RbdDemographicsReviewAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in RbdDemographicsReview._meta.fields]

admin.site.register(RbdDemographicsReview, RbdDemographicsReviewAdmin)
