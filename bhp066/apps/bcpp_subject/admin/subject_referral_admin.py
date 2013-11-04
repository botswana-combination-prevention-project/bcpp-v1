from collections import OrderedDict

from django.contrib import admin

from edc.export.actions import export_as_csv_action

from ..models import SubjectReferral
from ..forms import SubjectReferralForm
from ..filters import SubjectCommunityListFilter

from .subject_visit_model_admin import SubjectVisitModelAdmin


class SubjectReferralAdmin(SubjectVisitModelAdmin):

    form = SubjectReferralForm

    date_hierarchy = 'referral_appt_date'

    search_fields = ['subject_visit__appointment__registered_subject__first_name', 'subject_visit__appointment__registered_subject__subject_identifier']

    list_display = [
        'subject_visit',
        'report_datetime',
        'dashboard',
        'referral_codes',
        'referral_appt_date',
        'exported',
        'exported_datetime',
        'in_clinic_flag',
        ]

    list_filter = ['exported', 'in_clinic_flag', SubjectCommunityListFilter, 'referral_codes', 'report_datetime', 'referral_appt_date', 'exported_datetime', 'hostname_created']

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

    def get_actions(self, request):
        actions = super(SubjectReferralAdmin, self).get_actions(request)
        actions['export_as_csv_action'] = (  # This is a django SortedDict (function, name, short_description)
            export_as_csv_action(
                exclude=['id', 'exported', 'exported_datetime', self.visit_model_foreign_key, 'revision', 'hostname_created', 'hostname_modified', 'created', 'modified', 'user_created', 'user_modified', 'comment'],
                extra_fields=OrderedDict(
                    {'subject_identifier': self.visit_model_foreign_key + '__appointment__registered_subject__subject_identifier',
                     'first_name': self.visit_model_foreign_key + '__appointment__registered_subject__first_name',
                     'last_name': self.visit_model_foreign_key + '__appointment__registered_subject__last_name',
                     'initials': self.visit_model_foreign_key + '__appointment__registered_subject__initials',
                     'gender': self.visit_model_foreign_key + '__appointment__registered_subject__gender',
                     'dob': self.visit_model_foreign_key + '__appointment__registered_subject__dob',
                     'identity': self.visit_model_foreign_key + '__appointment__registered_subject__identity',
                     'identity_type': self.visit_model_foreign_key + '__appointment__registered_subject__identity_type',
                     })
                ),
                'export_as_csv_action',
                "Export Referrals to CSV")
        return actions

admin.site.register(SubjectReferral, SubjectReferralAdmin)
