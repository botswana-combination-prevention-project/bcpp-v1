from django.contrib import admin
from django.conf import settings
from edc_constants.constants import POS

from bhp066.apps.bcpp_survey.models import Survey

from ..classes import SubjectStatusHelper
from ..constants import ANNUAL
from ..forms import HivCareAdherenceForm
from ..models import HivCareAdherence

from .subject_admin_exclude_mixin import SubjectAdminExcludeMixin
from .subject_visit_model_admin import SubjectVisitModelAdmin


class HivCareAdherenceAdmin(SubjectAdminExcludeMixin, SubjectVisitModelAdmin):

    fields = [
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

    form = HivCareAdherenceForm

    radio_fields = {
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

    def get_custom_exclude(self, request, obj=None, visit_code=None):
        exclude = []
        visit_code = visit_code or self.get_visit_code(request, obj)
        if visit_code in self.visit_codes.get(ANNUAL):
            exclude = [
                "first_positive",
                "medical_care",
                "no_medical_care",
                "no_medical_care_other",
                "ever_recommended_arv",
                "ever_taken_arv",
                "why_no_arv",
                "why_no_arv_other"
                "first_arv"]
            if not Survey.objects.first_survey.survey_slug == settings.CURRENT_SURVEY:
                subject_visit = self.get_visit(request, obj)
                if subject_visit:
                    subject_helper = SubjectStatusHelper(subject_visit, use_baseline_visit=True)
                    if subject_helper.hiv_result == POS and not subject_helper.on_art:
                        exclude.pop('first_positive')
        return exclude

admin.site.register(HivCareAdherence, HivCareAdherenceAdmin)
