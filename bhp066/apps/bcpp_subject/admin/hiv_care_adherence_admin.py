from django.contrib import admin

from ..classes import SubjectStatusHelper
from ..forms import HivCareAdherenceForm
from ..models import HivCareAdherence, SubjectVisit

from edc.constants import POS

from .subject_visit_model_admin import SubjectVisitModelAdmin
from bhp066.apps.bcpp_subject.constants import ANNUAL_CODES, BASELINE_CODES

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

    @property
    def annual_fields(self):
        """Returns a subset of annual_fields if subject is POS and not on ART."""
        annual_fields = [f for f in self.baseline_fields if f not in [
             "first_positive", "medical_care", "no_medical_care", "no_medical_care_other",
             "ever_recommended_arv", "ever_taken_arv", "why_no_arv", "why_no_arv_other", "on_arv"]]
        if self.hiv_result_on_pos_and_subject_not_on_art:
            annual_fields = self.baseline_fields
            annual_fields.remove('first_positive')
        return annual_fields

    @property
    def hiv_result_on_pos_and_subject_not_on_art(self):
        try:
            baseline_subject_visit = SubjectVisit.objects.get(
                household_member__registered_subject=self.subject_visit.appointment.registered_subject,
                appointment__visit_definition__code=BASELINE_CODES)
        except SubjectVisit.DoesNotExist:
            baseline_subject_visit = None
        subject_helper = SubjectStatusHelper(baseline_subject_visit)
        return (subject_helper.hiv_result == POS and not subject_helper.on_art)


admin.site.register(HivCareAdherence, HivCareAdherenceAdmin)
