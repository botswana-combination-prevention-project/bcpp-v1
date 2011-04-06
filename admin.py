from django.contrib import admin
from bhp_common.models import MyModelAdmin, MyStackedInline
from models import SimpleAdverseEvent, DeathCauseInfo, DeathCauseCategory, DeathMedicalResponsibility, DeathReasonHospitalized, DeathForm

admin.site.register(DeathCauseInfo)
admin.site.register(DeathCauseCategory)
admin.site.register(DeathMedicalResponsibility)
admin.site.register(DeathReasonHospitalized)
admin.site.register(DeathForm)
admin.site.register(SimpleAdverseEvent)
