from django.contrib import admin
from ..models import HivCareAdherence
from ..forms import HivCareAdherenceForm
from .subject_visit_model_admin import SubjectVisitModelAdmin


class HivCareAdherenceAdmin(SubjectVisitModelAdmin):

    form = HivCareAdherenceForm
    fields = (
        "subject_visit",
        "first_positive",
        "medical_care",
        "no_medical_care",
        'ever_recommended_arv',
        'arv_naive',
        'why_no_arv',
        'why_no_arv_other',
        'first_arv',
        'on_arv',
        'arv_stop',
        'arv_stop_date',
        'arv_stop_other',
        'adherence_4_day',
        'adherence_4_wk',)
    radio_fields = {
        "medical_care": admin.VERTICAL,
        "no_medical_care": admin.VERTICAL,
        "ever_recommended_arv": admin.VERTICAL,
        "arv_naive": admin.VERTICAL,
        "why_no_arv": admin.VERTICAL,
        "on_arv": admin.VERTICAL,
        "arv_stop": admin.VERTICAL,
        "adherence_4_day": admin.VERTICAL,
        "adherence_4_wk": admin.VERTICAL, }
    instructions = [("Note to Interviewer: This section is only to be"
                             " completed by HIV-positive participants who knew"
                             " that they were HIV-positive before today."
                             " Section should be skipped for HIV-negative participants"
                             " and participants who first tested HIV-positive"
                             " today. Read to Participant: I am now going to"
                             " ask you some questions about care you may have"
                             " been given for your HIV infection.")]
admin.site.register(HivCareAdherence, HivCareAdherenceAdmin)
