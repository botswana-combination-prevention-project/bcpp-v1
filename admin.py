from django.contrib import admin
from bhp_common.models import MyModelAdmin, MyStackedInline
from models import RegisteredSubject, OffStudyReason, OffStudy, RandomizedSubject
from models import DeathCauseInfo, DeathCauseCategory, DeathMedicalResponsibility, DeathReasonHospitalized, DeathForm


class RegisteredSubjectAdmin (MyModelAdmin):

  list_display = (
        'subject_identifier',
        'subject_consent_id',        
        'first_name',
        'initials',
        'user_created',
        'created',        
    )   
admin.site.register(RegisteredSubject, RegisteredSubjectAdmin)

admin.site.register(RandomizedSubject)
admin.site.register(OffStudyReason)
admin.site.register(OffStudy)
admin.site.register(DeathCauseInfo)
admin.site.register(DeathCauseCategory)
admin.site.register(DeathMedicalResponsibility)
admin.site.register(DeathReasonHospitalized)
admin.site.register(DeathForm)
