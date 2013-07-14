from django.contrib import admin
from bcpp_subject.models import EnrolmentChecklist
from bcpp_subject.forms import EnrolmentChecklistForm
from registered_subject_model_admin import RegisteredSubjectModelAdmin


class EnrolmentChecklistAdmin(RegisteredSubjectModelAdmin):

    form = EnrolmentChecklistForm
    fields = (
        "registered_subject",
        "registration_datetime",
        "census_number",
        "mental_capacity",
        "incarceration",
        "citizen",
        "community_resident",
        "date_minor_signed",
        "date_guardian_signed",
        "date_consent_signed",)
    radio_fields = {
        "mental_capacity": admin.VERTICAL,
        "incarceration": admin.VERTICAL,
        "citizen": admin.VERTICAL,
        "community_resident": admin.VERTICAL, }
admin.site.register(EnrolmentChecklist, EnrolmentChecklistAdmin)
