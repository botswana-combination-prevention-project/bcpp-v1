from django.contrib import admin
from bhp_adverse.models import SimpleAdverseEvent, DeathCauseInfo, DeathCauseCategory, DeathMedicalResponsibility, DeathReasonHospitalized

admin.site.register(DeathCauseInfo)
admin.site.register(DeathCauseCategory)
admin.site.register(DeathMedicalResponsibility)
admin.site.register(DeathReasonHospitalized)
admin.site.register(SimpleAdverseEvent)
