from django.contrib import admin
from django.utils.translation import ugettext as _

from ..forms import AccessToCareForm
from ..models import AccessToCare

from .subject_visit_model_admin import SubjectVisitModelAdmin


class AccessToCareAdmin(SubjectVisitModelAdmin):

    form = AccessToCareForm

    fields = (
        "subject_visit",
        "report_datetime",
        "access_care",
        "access_care_other",
        "medical_care_access",
        "medical_care_access_other",
        "overall_access",
        "emergency_access",
        "expensive_access",
        "convenient_access",
        "whenever_access",
        "local_hiv_care",
    )
    radio_fields = {
        "access_care": admin.VERTICAL,
        "overall_access": admin.VERTICAL,
        "emergency_access": admin.VERTICAL,
        "expensive_access": admin.VERTICAL,
        "convenient_access": admin.VERTICAL,
        "whenever_access": admin.VERTICAL,
        "local_hiv_care": admin.VERTICAL}
    filter_horizontal = (
        "medical_care_access",)
    instructions = [_("<h5>Read to Participant</h5> Now, I will be asking you "
                      "about your preferences and options for accessing "
                      "health care when you need it.")]

admin.site.register(AccessToCare, AccessToCareAdmin)
