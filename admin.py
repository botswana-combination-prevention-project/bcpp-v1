from django.contrib import admin
from bhp_common.models import MyModelAdmin, MyStackedInline
from bhp_registration.utils import AllocateIdentifier
from models import BaseLocatorForm

class SubjectConsentAdminBase(MyModelAdmin):
  
    #def save_model(self, request, obj, form, change):
    #    obj.user_created = request.user
    #    obj.user_modified = request.user            
    #    obj.save()
    #    
    #    new_pk = obj.pk
    #    
    #    if not change:
    #        #allocate subject identifier
    #        obj = SubjectConsent.objects.get(pk=new_pk)
    #        obj.subject_identifier = AllocateIdentifier(new_pk, request.user)
    #        obj.save()

            
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
        'consent_datetime',
        'study_site',
        'gender',
        'dob',
        'is_dob_estimated',
        'identity',
        'identity_type',
        'may_store_samples',
        )
    radio_fields = {
        "gender":admin.VERTICAL,
        "study_site":admin.VERTICAL,
        "is_dob_estimated":admin.VERTICAL,
        "identity_type":admin.VERTICAL,
        "may_store_samples":admin.VERTICAL,
        }
        
#admin.site.register(SubjectConsent, SubjectConsentAdmin)


class BaseLocatorFormAdmin(MyModelAdmin):
    
    fields = (
        'date_signed',
        'mail_address',
        'care_clinic',
        'home_visit_permission',
        'physical_address',
        'may_follow_up',
        'subject_cell',
        'subject_cell_alt',
        'subject_phone',
        'subject_phone_alt',
        'may_call_work',
        'subject_work_place',
        'subject_work_phone',
        'may_contact_someone',
        'contact_name',
        'contact_rel',
        'contact_physical_address',
        'contact_cell',
        'contact_phone',
        'has_caretaker_alt',
        'caretaker_name',
        'caretaker_cell',
        'caretaker_tel',
        )
        
    radio_fields = {
        "home_visit_permission":admin.VERTICAL,
        "may_follow_up":admin.VERTICAL,
        "may_call_work":admin.VERTICAL,
        "may_contact_someone":admin.VERTICAL,  
        "has_caretaker_alt":admin.VERTICAL, 
              
        }                
#admin.site.register(BaseLocatorForm, BaseLocatorFormAdmin)

