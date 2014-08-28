from django.contrib import admin

from edc.base.modeladmin.admin import BaseModelAdmin

from ..forms import CorrectConsentForm
from ..models import CorrectConsent, SubjectConsent


class CorrectConsentAdmin(BaseModelAdmin):

    form = CorrectConsentForm

    fields = (
        'subject_consent',
        'report_datetime',
        'old_last_name',
        'new_last_name',
        'old_first_name',
        'new_first_name',
        'old_initials',
        'new_initials',
        'old_dob',
        'new_dob',
        'old_gender',
        'new_gender',
        'old_guardian_name',
        'new_guardian_name',
        'old_may_store_samples',
        'new_may_store_samples',
        'old_is_literate',
        'new_is_literate',
        )

    list_display = ('subject_consent', 'first_name', 'may_store_samples', 'is_literate')

    list_filter = ('report_datetime', 'created', 'modified')

    search_fields = ('subject_consent__subject_identifier', 'first_name')

    radio_fields = {
        'old_gender': admin.VERTICAL,
        'new_gender': admin.VERTICAL,
        'old_is_literate': admin.VERTICAL,
        'new_is_literate': admin.VERTICAL,
        'old_may_store_samples': admin.VERTICAL,
        'new_may_store_samples': admin.VERTICAL,
        }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "subject_consent":
            kwargs["queryset"] = SubjectConsent.objects.filter(id__exact=request.GET.get('subject_consent', 0))
        return super(CorrectConsentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
admin.site.register(CorrectConsent, CorrectConsentAdmin)
