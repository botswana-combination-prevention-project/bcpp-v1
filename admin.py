from django.contrib import admin
from bhp_common.models import MyModelAdmin, MyStackedInline
from bhp_registration.utils import AllocateIdentifier
from models import SubjectIdentifierAuditTrail, SubjectConsent
from models import LocatorForm  

class LocatorFormAdmin(MyModelAdmin):
    pass
admin.site.register(LocatorForm, LocatorFormAdmin)

class SubjectConsentAdmin(MyModelAdmin):
  
    def save_model(self, request, obj, form, change):
        obj.user_created = request.user
        obj.user_modified = request.user            
        obj.save()
        
        new_pk = obj.pk
        
        if not change:
            #allocate subject identifier
            obj = SubjectConsent.objects.get(pk=new_pk)
            obj.subject_identifier = AllocateIdentifier(new_pk, request.user)
            obj.save()

            
    #override to disallow subject to be changed
    def get_readonly_fields(self, request, obj = None):
        if obj: #In edit mode
            return ('subject_identifier','first_name','last_name','study_site','initials','consent_datetime',) + self.readonly_fields
        else:
            return ('subject_identifier',) + self.readonly_fields  
            
    fields = (
        'subject_identifier',
        'first_name',
        'last_name',
        'initials',
        'study_site',
        'consent_datetime',
        'omang',
        'gender',
        'dob',
        'is_dob_estimated',
        'may_store_samples',        
        'comment',
        )        

    radio_fields = {
        "gender":admin.VERTICAL,
        "study_site":admin.VERTICAL,
        "may_store_samples":admin.VERTICAL,
        "is_dob_estimated":admin.VERTICAL,                
        }        
        
admin.site.register(SubjectConsent, SubjectConsentAdmin)

class SubjectIdentifierAuditTrailAdmin(MyModelAdmin):
    list_display = (
        'subject_identifier',
        'first_name',
        'initials',
        'date_allocated',
        )
    list_per_page = 15
        
admin.site.register(SubjectIdentifierAuditTrail, SubjectIdentifierAuditTrailAdmin)

