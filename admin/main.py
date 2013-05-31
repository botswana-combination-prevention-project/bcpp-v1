from django.contrib import admin
from bhp_base_admin.admin import BaseModelAdmin
from bcpp_list.models import ElectricalAppliances, TransportMode, LiveWith, NeighbourhoodProblems, CicumcisionBenefits, FamilyPlanning, MedicalCareAccess, HouseholdSurveyCode, HouseholdSurveyReason, HouseholdSurveySource, SurveyGroup, HouseholdStructureRelation, HouseholdSurveyStatus, SubjectAbsenteeReason, SubjectMovedReason


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


class CicumcisionBenefitsAdmin(BaseModelAdmin):
    pass
admin.site.register(CicumcisionBenefits, CicumcisionBenefitsAdmin)


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
