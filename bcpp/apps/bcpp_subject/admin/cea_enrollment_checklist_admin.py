from django.contrib import admin

from ..models import CeaEnrollmentChecklist
from ..forms import CeaEnrollmentChecklistForm

from .registered_subject_model_admin import RegisteredSubjectModelAdmin


class CeaEnrollmentChecklistAdmin(RegisteredSubjectModelAdmin):

    form = CeaEnrollmentChecklistForm
    fields = (
        "registered_subject",
        "report_datetime",
        "citizen",
        "legal_marriage",
        "marriage_certificate",
        "marriage_certificate_no",
        "community_resident",
        "enrollment_reason",
        "cd4_date",
        "cd4_count",
        "opportunistic_illness",
        "diagnosis_date",
        "date_signed",)
    radio_fields = {
        "citizen": admin.VERTICAL,
        "legal_marriage": admin.VERTICAL,
        "marriage_certificate": admin.VERTICAL,
        "community_resident": admin.VERTICAL,
        "enrollment_reason": admin.VERTICAL,
        "opportunistic_illness": admin.VERTICAL, }
admin.site.register(CeaEnrollmentChecklist, CeaEnrollmentChecklistAdmin)
