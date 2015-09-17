from django.contrib import admin
from edc.base.modeladmin.admin import BaseModelAdmin
from bhp066.apps.bcpp_list.models import (
    ElectricalAppliances, TransportMode, LiveWith, NeighbourhoodProblems, CircumcisionBenefits,
    FamilyPlanning, MedicalCareAccess, PartnerResidency, HeartDisease, Diagnoses, Religion,
    EthnicGroups, StiIllnesses, ResidentMostLikely)


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


class StiIllnessesAdmin(BaseModelAdmin):
    pass
admin.site.register(StiIllnesses, StiIllnessesAdmin)


class ResidentMostLikelyAdmin(BaseModelAdmin):
    pass
admin.site.register(ResidentMostLikely, ResidentMostLikelyAdmin)
