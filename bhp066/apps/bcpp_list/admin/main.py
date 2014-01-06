from django.contrib import admin
from edc.base.admin.admin import BaseModelAdmin
from apps.bcpp_list.models import (ElectricalAppliances, TransportMode, LiveWith,
                              NeighbourhoodProblems, CircumcisionBenefits,
                              FamilyPlanning, MedicalCareAccess, HouseholdSurveyCode,
                              HouseholdSurveyReason, HouseholdSurveySource,
                              SurveyGroup, HouseholdStructureRelation,
                              HouseholdSurveyStatus, SubjectAbsenteeReason,
                              SubjectMovedReason, SubjectUndecidedReason,
                              PartnerResidency, HeartDisease,
                              Diagnoses, Religion, EthnicGroups, ReferredTo,
                              ReferredFor, StiIllnesses)


class ElectricalAppliancesAdmin(BaseModelAdmin):
    pass
admin.site.register(ElectricalAppliances, ElectricalAppliancesAdmin)


class TransportModeAdmin(BaseModelAdmin):
    pass
admin.site.register(TransportMode, TransportModeAdmin)


class LiveWithAdmin(BaseModelAdmin):
    pass
admin.site.register(LiveWith, LiveWithAdmin)


class NeighbourhoodProblemsAdmin(BaseModelAdmin):
    pass
admin.site.register(NeighbourhoodProblems, NeighbourhoodProblemsAdmin)


class CircumcisionBenefitsAdmin(BaseModelAdmin):
    pass
admin.site.register(CircumcisionBenefits, CircumcisionBenefitsAdmin)


class FamilyPlanningAdmin(BaseModelAdmin):
    pass
admin.site.register(FamilyPlanning, FamilyPlanningAdmin)


class MedicalCareAccessAdmin(BaseModelAdmin):
    pass
admin.site.register(MedicalCareAccess, MedicalCareAccessAdmin)


class HouseholdSurveyCodeAdmin(BaseModelAdmin):
    pass
admin.site.register(HouseholdSurveyCode, HouseholdSurveyCodeAdmin)


class HouseholdSurveyReasonAdmin(BaseModelAdmin):
    pass
admin.site.register(HouseholdSurveyReason, HouseholdSurveyReasonAdmin)


class HouseholdSurveySourceAdmin(BaseModelAdmin):
    pass
admin.site.register(HouseholdSurveySource, HouseholdSurveySourceAdmin)


class SurveyGroupAdmin(BaseModelAdmin):
    pass
admin.site.register(SurveyGroup, SurveyGroupAdmin)


class HouseholdStructureRelationAdmin(BaseModelAdmin):
    pass
admin.site.register(HouseholdStructureRelation, HouseholdStructureRelationAdmin)


class HouseholdSurveyStatusAdmin(BaseModelAdmin):
    pass
admin.site.register(HouseholdSurveyStatus, HouseholdSurveyStatusAdmin)


class SubjectAbsenteeReasonAdmin(BaseModelAdmin):
    pass
admin.site.register(SubjectAbsenteeReason, SubjectAbsenteeReasonAdmin)


class SubjectMovedReasonAdmin(BaseModelAdmin):
    pass
admin.site.register(SubjectMovedReason, SubjectMovedReasonAdmin)


class SubjectUndecidedReasonAdmin(BaseModelAdmin):
    pass
admin.site.register(SubjectUndecidedReason, SubjectUndecidedReasonAdmin)


class PartnerResidencyAdmin(BaseModelAdmin):
    pass
admin.site.register(PartnerResidency, PartnerResidencyAdmin)


class HeartDiseaseAdmin(BaseModelAdmin):
    pass
admin.site.register(HeartDisease, HeartDiseaseAdmin)


class DiagnosesAdmin(BaseModelAdmin):
    pass
admin.site.register(Diagnoses, DiagnosesAdmin)


class ReligionAdmin(BaseModelAdmin):
    pass
admin.site.register(Religion, ReligionAdmin)


class EthnicGroupsAdmin(BaseModelAdmin):
    pass
admin.site.register(EthnicGroups, EthnicGroupsAdmin)


class ReferredForAdmin(BaseModelAdmin):
    pass
admin.site.register(ReferredFor, ReferredForAdmin)


class ReferredToAdmin(BaseModelAdmin):
    pass
admin.site.register(ReferredTo, ReferredToAdmin)


class StiIllnessesAdmin(BaseModelAdmin):
    pass
admin.site.register(StiIllnesses, StiIllnessesAdmin)
