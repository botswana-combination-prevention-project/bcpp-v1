from django.contrib import admin
from ..models import  HicEnrollment
from ..forms import HicEnrollmentForm
from .subject_visit_model_admin import SubjectVisitModelAdmin
from ..filters import HicEnrollmentFilter


class HicEnrollmentAdmin(SubjectVisitModelAdmin):

    form = HicEnrollmentForm
    fields = (
        "subject_visit",
        "dob",
        "hic_permission",
        "permanent_resident",
        "intend_residency",
        "hiv_status_today",
        "household_residency",
        "citizen_or_spouse",
        "locator_information",
        "consent_datetime",
        )
    radio_fields = {
        'hic_permission': admin.VERTICAL,
        #'permanent_resident': admin.VERTICAL,
        #'intend_residency': admin.VERTICAL,
        #'household_residency': admin.VERTICAL,
        #'citizen_or_spouse': admin.VERTICAL,
        #'locator_information': admin.VERTICAL,
        }
    list_display = (
        'subject_visit',
        'dob',
        'hic_permission',
        'intend_residency',
        'permanent_resident',
        'hiv_status_today',
        'citizen_or_spouse',
        'consent_datetime',
        )
    list_filter = ('consent_datetime', HicEnrollmentFilter,)
    readonly_fields = (
        "dob",
        "permanent_resident",
        "intend_residency",
        "hiv_status_today",
        "household_residency",
        "citizen_or_spouse",
        "locator_information",
        "consent_datetime",
        )
admin.site.register(HicEnrollment, HicEnrollmentAdmin)
