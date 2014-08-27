from django.contrib import admin

from ..forms import CorrectConsentForm
from apps.bcpp_household.admin.base_household_model_admin import BaseHouseholdModelAdmin
from apps.bcpp_subject.models.subject_consent import SubjectConsent

from ..models import CorrectConsent


class CorrectConsentAdmin(BaseHouseholdModelAdmin):

    form = CorrectConsentForm

    fields = (
        'subject_consent',
        'report_datetime',
        'last_name',
        'last_name_old',
        'first_name',
        'first_name_old',
        'initials',
        'initials_old',
        'dob',
        'dob_old',
        'gender',
        'gender_old',
        'guardian_name',
        'guardian_name_old',
        'may_store_samples',
        'may_store_samples_old',
        'is_literate',
        'is_literate_old',
        )

    list_display = ('subject_consent', 'first_name', 'may_store_samples', 'is_literate')

    list_filter = ('report_datetime', 'created', 'modified')

    search_fields = ('subject_consent__subject_identifier', 'first_name')

    radio_fields = {
        'gender': admin.VERTICAL,
        'gender_old': admin.VERTICAL,
        'is_literate': admin.VERTICAL,
        'is_literate_old': admin.VERTICAL,
        'may_store_samples': admin.VERTICAL,
        'may_store_samples_old': admin.VERTICAL,
        }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "plot":
            kwargs["queryset"] = SubjectConsent.objects.filter(id__exact=request.GET.get('subject_consent', 0))
        return super(CorrectConsentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
admin.site.register(CorrectConsent, CorrectConsentAdmin)
