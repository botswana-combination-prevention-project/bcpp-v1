from django.contrib import admin

from ..forms import CorrectConsentForm
from apps.bcpp_household.admin.base_household_model_admin import BaseHouseholdModelAdmin

from ..models import CorrectConsent


class CorrectConsentAdmin(BaseHouseholdModelAdmin):

    form = CorrectConsentForm

    fields = (
        'subject_identifier',
        'last_name',
        'first_name',
        'initials',
        'dob',
        'gender',
        'guardian_name',
        'is_literate',
        'may_store_samples'
        )

    radio_fields = {
        'gender': admin.VERTICAL,
        'gender': admin.VERTICAL,
        'is_literate': admin.VERTICAL,
        'may_store_samples': admin.VERTICAL,
        }

admin.site.register(CorrectConsent, CorrectConsentAdmin)
