from django.contrib import admin

from .subject_visit_model_admin import SubjectVisitModelAdmin

from ..actions import update_referrals, call_participant, update_referrals_for_hic_action
from ..filters import HicEnrollmentFilter, MayContactFilter
from ..forms import HicEnrollmentForm
from ..models import HicEnrollment


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
        }

    list_display = (
        'subject_visit',
        'dob',
        'age',
        'may_contact',
        'call_attempts',
        'call_outcome',
        'bhs_referral_code',
        'hostname_created',
        'user_created',
        'intend_residency',
        'permanent_resident',
        'citizen_or_spouse',
        'consent_datetime',
        )
    list_filter = ('consent_datetime',
                   HicEnrollmentFilter,
                   MayContactFilter,
                   'call_attempts',
                   'bhs_referral_code',
                   'hostname_created',
                   'user_created',
                   )

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

    actions = [update_referrals, call_participant, update_referrals_for_hic_action]

admin.site.register(HicEnrollment, HicEnrollmentAdmin)
