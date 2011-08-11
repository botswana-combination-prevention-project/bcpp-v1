from django.contrib import admin
from bhp_common.models import MyModelAdmin, MyStackedInline
from models import RegisteredSubject, RandomizedSubject, SubjectIdentifierAuditTrail

class RegisteredSubjectAdmin (MyModelAdmin):

    list_display = (
        'subject_identifier',
        'sid',        
        'first_name',
        'initials',
        'gender',
        'subject_type',
        'user_created',
        'created',
        'sid',        
    )   
    
    readonly_fields = (
        'subject_identifier',
        )

    search_fields = ('subject_identifier', 'first_name', 'initials', 'sid')    

    
    list_filter = ('subject_type',)
    
admin.site.register(RegisteredSubject, RegisteredSubjectAdmin)

admin.site.register(RandomizedSubject)


class SubjectIdentifierAuditTrailAdmin(MyModelAdmin):
    list_display = (
        'subject_identifier',
        'first_name',
        'initials',
        'date_allocated',
        )
    list_per_page = 15
        
admin.site.register(SubjectIdentifierAuditTrail, SubjectIdentifierAuditTrailAdmin)

