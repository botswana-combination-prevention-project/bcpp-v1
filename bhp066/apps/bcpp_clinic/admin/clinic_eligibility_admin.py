from django.contrib import admin
from edc.base.admin.admin import BaseModelAdmin
from ..models import ClinicEligibility
from ..forms import ClinicEligibilityForm


class ClinicEligibilityAdmin(BaseModelAdmin):

    form = ClinicEligibilityForm

    instructions = ['This form is a tool to assist the Interviewer to confirm the Eligibility status of the subject.']

    fields = (
        'registered_subject',
        'dob',
        "part_time_resident",
        "hiv_status",)
    radio_fields = {
        "part_time_resident": admin.VERTICAL,
        "hiv_status": admin.VERTICAL, }

admin.site.register(ClinicEligibility, ClinicEligibilityAdmin)
