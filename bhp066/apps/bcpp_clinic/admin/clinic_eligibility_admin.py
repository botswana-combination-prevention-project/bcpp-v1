from django.contrib import admin

from ..forms import ClinicEligibilityForm
from ..models import ClinicEligibility

from edc.base.modeladmin.admin import BaseModelAdmin


class ClinicEligibilityAdmin(BaseModelAdmin):

    form = ClinicEligibilityForm

    instructions = ['This form is a tool to assist the Interviewer to confirm the Eligibility status of the subject.']

    fields = (
        'first_name',
        'initials',
        'gender',
        'dob',
        'inability_to_participate',
        'has_identity',
        'citizen',
        "legal_marriage",
        'marriage_certificate',
        "part_time_resident",
        'literacy',
        "hiv_status",)
    radio_fields = {
        "part_time_resident": admin.VERTICAL,
        "inability_to_participate": admin.VERTICAL,
        "hiv_status": admin.VERTICAL,
        "legal_marriage": admin.VERTICAL,
        "citizen": admin.VERTICAL,
        "marriage_certificate": admin.VERTICAL,
        "literacy": admin.VERTICAL}
    list_display = ('registered_subject', 'is_eligible', 'registration_datetime')
    list_filter = ('is_eligible', )
    search_fields = (
        'registered_subject__subject_identifier',
        'initials',
        'first_name',
        )

admin.site.register(ClinicEligibility, ClinicEligibilityAdmin)
