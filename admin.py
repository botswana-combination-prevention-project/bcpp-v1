from django.contrib import admin
from bhp_base_admin.admin import BaseModelAdmin
from lab_result.models import Result
from lab_patient.models import Patient
from lab_patient.forms import PatientForm


class PatientAdmin(BaseModelAdmin):

    form = PatientForm

    def change_view(self, request, object_id, extra_context=None):

        change_view_result = super(PatientAdmin, self).change_view(request, object_id, extra_context)
        #oPatient = Patient.objects.get(pk=object_id)
        if request.GET.get('return_object') == 'result':
            try:
                result = Result.objects.get(pk=request.GET.get('object_id'))
                change_view_result['Location'] = result.get_document_url()
            except:
                pass
        return result

    list_display = ('subject_identifier', 'initials', 'gender', 'dob', 'created', 'modified')
    ordering = ['created']
    radio_fields = {
        "gender": admin.VERTICAL,
        "is_dob_estimated": admin.VERTICAL,
        "hiv_status": admin.VERTICAL,
        "art_status": admin.VERTICAL,
        }
    search_fields = ['subject_identifier']
    list_per_page = 25
admin.site.register(Patient, PatientAdmin)
