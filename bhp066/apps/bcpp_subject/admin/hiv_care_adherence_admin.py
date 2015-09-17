from django.contrib import admin
from django.conf import settings
from edc.constants import POS

from bhp066.apps.bcpp_survey.models import Survey

from ..classes import SubjectStatusHelper
from ..forms import HivCareAdherenceForm
from ..models import HivCareAdherence

from .subject_visit_model_admin import SubjectVisitModelAdmin


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

    annual_fields = [f for f in baseline_fields if f not in [
        "first_positive", "medical_care", "no_medical_care", "no_medical_care_other", "ever_recommended_arv", "ever_taken_arv",
        "why_no_arv", "first_arv"]]

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

    @property
    def annual_fields(self):
        """Returns a subset of annual_fields if subject is POS and on ART."""
        if not Survey.objects.first_survey.survey_slug == settings.CURRENT_SURVEY:
            if self.hiv_result_on_pos_and_subject_not_on_art:
                try:
                    annual_fields = self.baseline_fields
                    annual_fields.remove('first_positive')
                except ValueError:
                    pass
            elif self.hiv_result_on_pos_and_subject_on_art:
                annual_fields = [f for f in self.baseline_fields if f not in [
                    "first_positive", "medical_care", "no_medical_care", "ever_recommended_arv", "ever_taken_arv",
                    "why_no_arv", "first_arv", "no_medical_care_other", "why_no_arv_other"]]
            else:
                annual_fields = self.baseline_fields
        else:
            return self.baseline_fields

        return annual_fields

    @property
    def hiv_result_on_pos_and_subject_not_on_art(self):
        subject_helper = SubjectStatusHelper(self.subject_visit, use_baseline_visit=True)
        return (subject_helper.hiv_result == POS and not subject_helper.on_art)

    @property
    def hiv_result_on_pos_and_subject_on_art(self):
        subject_helper = SubjectStatusHelper(self.subject_visit, use_baseline_visit=True)
        return (subject_helper.hiv_result == POS and subject_helper.on_art)


admin.site.register(HivCareAdherence, HivCareAdherenceAdmin)
