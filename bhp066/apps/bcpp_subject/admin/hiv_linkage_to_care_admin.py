from django.contrib import admin

from edc_field_label.admin_mixin import ModifyFormLabelMixin

from ..forms import HivLinkageToCareForm
from ..models import HivLinkageToCare

from .subject_visit_model_admin import SubjectVisitModelAdmin


class HivLinkageToCareAdmin(ModifyFormLabelMixin, SubjectVisitModelAdmin):

    replacements = {
        'first_rep': {
            'field_attr': 'kept_appt',
            'placeholder': 'last_visit_date',
            'replacement_attr': 'report_datetime',
            'attr': 'previous_visit',
        },
        'second_rep': {
            'field_attr': 'kept_appt',
            'placeholder': 'last_appt_date',
            'replacement_attr': 'appt_datetime',
            'attr': 'previous_appt',
        },
        'third_rep': {
            'field_attr': 'recommended_therapy',
            'placeholder': 'last_visit_date',
            'replacement_attr': 'report_datetime',
            'attr': 'previous_visit',
        },
        'forth_rep': {
            'field_attr': 'startered_therapy',
            'placeholder': 'last_visit_date',
            'replacement_attr': 'report_datetime',
            'attr': 'previous_visit',
        },
        'fifth_rep': {
            'field_attr': 'clinic_first_date',
            'placeholder': 'community_name',
            'replacement_attr': 'community',
            'attr': 'last_community',
        },
    }

    form = HivLinkageToCareForm

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
