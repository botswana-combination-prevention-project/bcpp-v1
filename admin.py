from django.contrib import admin
from bhp_common.models import MyModelAdmin, MyStackedInline
from models import RegisteredSubject, OffStudyReason, OffStudy, RandomizedSubject

class RegisteredSubjectAdmin (MyModelAdmin):

  list_display = (
        'subject_identifier',
        'subject_consent_id',        
        'first_name',
        'initials',
        'subject_type',
        'user_created',
        'created',        
    )   
admin.site.register(RegisteredSubject, RegisteredSubjectAdmin)

admin.site.register(RandomizedSubject)

admin.site.register(OffStudyReason)

admin.site.register(OffStudy)

