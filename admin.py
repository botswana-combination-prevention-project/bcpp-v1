from django.contrib import admin
from bhp_common.models import MyModelAdmin
from models import RegisteredSubject, SubjectIdentifierAuditTrail
from forms import RegisteredSubjectForm


class RegisteredSubjectAdmin (MyModelAdmin):

    form = RegisteredSubjectForm
 
    list_display = (
        'subject_identifier',
        'first_name',
        'initials',
        'gender',
        'subject_type',
        'sid',     
        'registration_status',           
        'study_site',
        'user_created',
        'created',

    )   
    
    readonly_fields = (
        'subject_identifier',
        )

    search_fields = ('subject_identifier', 'first_name', 'initials', 'sid', 'identity', 'id')    

    
    list_filter = ('subject_type', 'registration_status', 'registration_datetime','gender','study_site', 'hiv_status', 'survival_status', 'may_store_samples','hostname_created')
    
admin.site.register(RegisteredSubject, RegisteredSubjectAdmin)


class SubjectIdentifierAuditTrailAdmin(MyModelAdmin):
    
    list_display = (
        'subject_identifier',
        'date_allocated',
        )
    list_per_page = 15
        
admin.site.register(SubjectIdentifierAuditTrail, SubjectIdentifierAuditTrailAdmin)

