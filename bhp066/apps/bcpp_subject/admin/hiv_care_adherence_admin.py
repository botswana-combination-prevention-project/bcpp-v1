from django.contrib import admin

from ..models import HivCareAdherence #, SubjectVisit
from ..forms import HivCareAdherenceForm

from .subject_visit_model_admin import SubjectVisitModelAdmin

#from ..classes import HivCareAdherenceHelper


class HivCareAdherenceAdmin(SubjectVisitModelAdmin):

    baseline_fields = [
        "subject_visit",
        "first_positive",
        "medical_care",
        "no_medical_care",
        "no_medical_care_other",
        'ever_recommended_arv',
        'ever_taken_arv',
        'why_no_arv',
        'why_no_arv_other',
        'first_arv',
        'on_arv',
        'arv_evidence',
        'clinic_receiving_from',
        'next_appointment_date',
        'arv_stop_date',
        'arv_stop',
        'arv_stop_other',
        'adherence_4_day',
        'adherence_4_wk']

    annual_fields = [f for f in baseline_fields if f not in ["first_positive", "medical_care", "no_medical_care", "ever_recommended_arv", "ever_taken_arv", "why_no_arv", "on_arv"]]

    form = HivCareAdherenceForm

    baseline_radio_fields = {
        "medical_care": admin.VERTICAL,
        "no_medical_care": admin.VERTICAL,
        "ever_recommended_arv": admin.VERTICAL,
        "ever_taken_arv": admin.VERTICAL,
        "why_no_arv": admin.VERTICAL,
        "on_arv": admin.VERTICAL,
        "arv_stop": admin.VERTICAL,
        "adherence_4_day": admin.VERTICAL,
        "adherence_4_wk": admin.VERTICAL,
        "arv_evidence": admin.VERTICAL}

    annual_radio_fields = baseline_radio_fields

    instructions = [("Note to Interviewer: This section is only to be"
                     " completed by HIV-positive participants who knew"
                     " that they were HIV-positive before today."
                     " Section should be skipped for HIV-negative participants"
                     " and participants who first tested HIV-positive"
                     " today. Read to Participant: I am now going to"
                     " ask you some questions about care you may have"
                     " been given for your HIV infection.")]
    list_display = (
        'subject_visit',
        'on_arv',
        'arv_evidence',
        'ever_taken_arv',
        )

    list_filter = (
        'on_arv',
        'arv_evidence',
        'ever_taken_arv',
        )

#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name == "subject_visit":
#             if request.GET.get('subject_visit'):
#                 kwargs["queryset"] = SubjectVisit.objects.filter(id=request.GET.get('subject_visit'))
                #visit_instance = SubjectVisit.objects.get(id=request.GET.get('subject_visit'))
                #hiv_care_adherence_helper = HivCareAdherenceHelper(visit_instance)
                #self.annual_fields = hiv_care_adherence_helper.annual_fields_pos_and_art if hiv_care_adherence_helper.annual_fields_pos_and_art else self.annual_fields
                #self.annual_radio_fields = hiv_care_adherence_helper.annual_radio_fields if hiv_care_adherence_helper.annual_fields_pos_and_art else self.annual_radio_fields

admin.site.register(HivCareAdherence, HivCareAdherenceAdmin)
