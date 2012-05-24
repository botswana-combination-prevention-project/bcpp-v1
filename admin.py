from django.contrib import admin
from bhp_common.models import MyModelAdmin
#from bhp_registration.utils import AllocateIdentifier
#from models import BaseLocator

class SubjectConsentAdminBase(MyModelAdmin):

    def __init__(self, *args, **kwargs):

        super(SubjectConsentAdminBase, self).__init__(*args, **kwargs)
                
        self.search_fields = ['id', 'subject_identifier','first_name', 'last_name', 'identity',] 
        
        self.list_display = ['subject_identifier','first_name','initials','gender','dob', 
                             'consent_datetime','created', 'modified', 'user_created', 'user_modified',]    
        
        self.list_filter = [
            'gender',
            'study_site',
            'consent_datetime', 
            'created', 
            'modified', 
            'user_created',
            'user_modified',
            'hostname_created',
            ]

        #self.actions.append(export_as_csv_action("CSV Export: ...with visit and demographics", 
        #    fields=[], 
        #    exclude=['id',],        
        #    extra_fields=[
        #        {'dob': self.visit_model_foreign_key+'__appointment__registered_subject__dob'},                                    
        #        {'visit_reason': self.visit_model_foreign_key+'__reason'},
        #        {'visit_status': self.visit_model_foreign_key+'__appointment__appt_status'},
        #        {'visit': self.visit_model_foreign_key+'__appointment__visit_definition__code'},
        #        {'visit_instance': self.visit_model_foreign_key+'__appointment__visit_instance'},                                                                    
        #        ],
        #    ))


  
    #override to disallow subject to be changed
    def get_readonly_fields(self, request, obj = None):
        if obj: #In edit mode
            return (
                'subject_identifier',
                'first_name',
                'last_name',
                'study_site',
                #'initials',
                'consent_datetime',) + self.readonly_fields
        else:
            return ('subject_identifier',) + self.readonly_fields  
            
    fields = [
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
        'guardian_name',
        'may_store_samples',
        'comment',
        ]
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
        'subject_consent',
        'date_signed',
        'mail_address',
        #'care_clinic',
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

