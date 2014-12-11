from django.contrib import admin
from django.utils.translation import ugettext as _

# from edc.apps.admin_supplemental_fields.admin import SupplementalModelAdminMixin
# from edc.apps.admin_supplemental_fields.classes import SupplementalFields

from apps.bcpp_subject.forms import AccessToCareForm

from .subject_visit_model_admin import SubjectVisitModelAdmin

from ..models import AccessToCare


# Access to Care [AC]: 10% in pretest, 9% in BHS and all follow-up
class AccessToCareAdmin(SubjectVisitModelAdmin):

    form = AccessToCareForm
#     supplemental_fields = SupplementalFields(
#         ('access_care',
#          'access_care_other',
#          'medical_care_access',
#          'medical_care_access_other',
#          'overall_access',
#          'emergency_access',
#          'expensive_access',
#          'convenient_access',
#          'whenever_access',
#          'local_hiv_care'), p=0.09, group='AC', grouping_field='subject_visit')
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
