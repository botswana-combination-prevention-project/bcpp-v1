from django.contrib import admin
from registered_subject_model_admin import RegisteredSubjectModelAdmin
from bcpp_subject.models import CeaEnrolmentChecklist
from bcpp_subject.forms import CeaEnrolmentChecklistForm


class CeaEnrolmentChecklistAdmin(RegisteredSubjectModelAdmin):

    form = CeaEnrolmentChecklistForm
    fields = (
        "registered_subject",
        "report_datetime",
        "citizen",
        "legal_marriage",
        "marriage_certificate",
        "marriage_certificate_no",
        "community_resident",
        "enrolment_reason",
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
        "enrolment_reason": admin.VERTICAL,
        "opportunistic_illness": admin.VERTICAL, }
admin.site.register(CeaEnrolmentChecklist, CeaEnrolmentChecklistAdmin)
