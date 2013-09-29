from django.contrib import admin
from edc_core.bhp_supplemental_fields.classes import SupplementalFields
from bcpp_subject.models import AccessToCare
from bcpp_subject.forms import AccessToCareForm
from .subject_visit_model_admin import SubjectVisitModelAdmin


#Access to Care [AC]: 10% in pretest, 9% in BHS and all follow-up
class AccessToCareAdmin(SubjectVisitModelAdmin):

    form = AccessToCareForm
    supplemental_fields = SupplementalFields(
        ('access_care',
        'access_care_other',
        'medical_care_access',
        'medical_care_access_other',
        'overall_access',
        'emergency_access',
        'expensive_access',
        'convenient_access',
        'whenever_access',
        'local_hiv_care'), p=0.09, group='AC')
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
    instructions = [("Read to Participant: Now, I will be asking you "
                             "about your preferences and options for accessing "
                             "health care when you need it.")]

admin.site.register(AccessToCare, AccessToCareAdmin)
