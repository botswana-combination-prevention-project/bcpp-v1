from django.contrib import admin

from django.utils import timezone

from ..forms import HivLinkageToCareForm
from ..models import HivLinkageToCare

from .subject_visit_model_admin import SubjectVisitModelAdmin
from .modify_form_labels_mixin import ModifyFormLabelMixin
from ..models import SubjectConsent, SubjectVisit


def kept_appt_datetime():
        return timezone.now()


class HivLinkageToCareAdmin(ModifyFormLabelMixin, SubjectVisitModelAdmin):

    form = HivLinkageToCareForm
    # QUERY_MODEL_PARAMETERS = {"field_name_to_modify_lable": [query_model, "replacement_model_field_attribute", "foreinkey_model", "foreign_key_field_attribute", "query_model_field_attribute"]}
    QUERY_MODEL_PARAMETERS = {"kept_appt": [SubjectConsent, "consent_datetime", SubjectVisit, "subject_visit", "subject_identifier"],
                              "startered_therapy": [SubjectConsent, "consent_datetime", SubjectVisit, "subject_visit", "subject_identifier"]}

    fields = (
        "subject_visit",
        "report_datetime",
        "kept_appt",
        "diff_clininc",
        "left_clininc",
        "clinic_first_date",
        "evidence_type_clinicdate",
        "evidence_type_clinicdate_other",
        "recommended_therapy",
        "reason_recommended",
        "reason_recommended_other",
        "startered_therapy",
        "startered_therapy_date",
        "start_therapy_clininc",
        "start_therapy_clininc_other",
        "not_refered_clininc",
        "evidence_not_refered",
        "evidence_not_refered_other",
    )
    radio_fields = {
        "kept_appt": admin.VERTICAL,
        "evidence_type_clinicdate": admin.VERTICAL,
        "recommended_therapy": admin.VERTICAL,
        "reason_recommended": admin.VERTICAL,
        "startered_therapy": admin.VERTICAL,
        "start_therapy_clininc": admin.VERTICAL,
        "evidence_not_refered": admin.VERTICAL}

admin.site.register(HivLinkageToCare, HivLinkageToCareAdmin)
