from django.contrib import admin
from bhp_common.models import MyModelAdmin, MyStackedInline
from lab_result.models import Result
from lab_patient.models import Patient, SimpleConsent
from lab_patient.forms import PatientForm


class PatientAdmin(MyModelAdmin):
    
    form= PatientForm
    
    
    def change_view(self, request, object_id, extra_context=None):

        result = super(PatientAdmin, self).change_view(request, object_id, extra_context)
        #oPatient = Patient.objects.get(pk=object_id)
        if request.GET.get('return_object')=='result': 
            try:
                oResult = Result.objects.get(pk=request.GET.get('object_id'))            
                result['Location'] = oResult.get_document_url()
            except:
                pass
        #elif not request.POST.has_key('_addanother') and not request.POST.has_key('_continue'):
        #    result['Location'] = oPatient.get_result_document_url()
        return result

    
    list_display = ('subject_identifier', 'initials', 'gender', 'dob', 'created', 'modified')

    ordering = ['created']

    radio_fields = { 
        "gender":admin.VERTICAL,
        "is_dob_estimated":admin.VERTICAL,        
        "hiv_status":admin.VERTICAL,
        "art_status":admin.VERTICAL,                        
        }       
    search_fields = ['subject_identifier']
    
    list_per_page = 25

admin.site.register(Patient, PatientAdmin)


class SimpleConsentAdmin(MyModelAdmin):

    radio_fields = { 
        "may_store_samples":admin.VERTICAL,
        }       

admin.site.register(SimpleConsent, SimpleConsentAdmin)


