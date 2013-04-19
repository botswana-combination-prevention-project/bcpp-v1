from django.contrib import admin
from bhp_base_model.classes import BaseModelAdmin
from bcpp_list.models import ElectricalAppliances, TransportMode, LiveWith, NeighbourhoodProblems


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
