from django.contrib import admin

from ..models import SubjectReferral
from ..forms import SubjectReferralForm

from .subject_visit_model_admin import SubjectVisitModelAdmin


class SubjectReferralAdmin(SubjectVisitModelAdmin):

    form = SubjectReferralForm

    search_fields = ['subject_visit__appointment__registered_subject__first_name', 'subject_visit__appointment__registered_subject__subject_identifier']

    list_display = ['referral_codes']

    list_filter = ('referral_codes')

    fields = (
        'subject_visit',
        'report_datetime',
        'referral_codes',
        'referral_appt_date',
        'referral_clinic',
        'comment'
        )
    radio_fields = {
        "referral_codes": admin.VERTICAL,
        "referral_clinic": admin.VERTICAL,
        }
#     readonly_fields = ('referral_codes')

admin.site.register(SubjectReferral, SubjectReferralAdmin)
