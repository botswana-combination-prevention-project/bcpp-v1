from django.contrib import admin
from subject_visit_model_admin import SubjectVisitModelAdmin
from bcpp_subject.models import HivCareAdherence
from bcpp_subject.forms import HivCareAdherenceForm


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
admin.site.register(HivCareAdherence, HivCareAdherenceAdmin)
