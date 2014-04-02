from collections import OrderedDict

from django.contrib import admin

from edc.export.actions import export_as_csv_action

from ..models import SubjectReferral, SubjectReferralReview
from ..forms import SubjectReferralForm
from ..filters import SubjectCommunityListFilter, SubjectReferralIsReferredListFilter

from .subject_visit_model_admin import SubjectVisitModelAdmin

# for subject_visit in SubjectVisit.objects.all():
#     SubjectReferral.objects.create(subject_visit=subject_visit, report_datetime=subject_visit.get_report_datetime(), subject_referred='Yes', referral_clinic='Otse', referral_appt_date=datetime(2014,4,7))


class SubjectReferralAdmin(SubjectVisitModelAdmin):

    form = SubjectReferralForm

    date_hierarchy = 'referral_appt_date'

    search_fields = ['subject_visit__appointment__registered_subject__first_name', 'subject_visit__appointment__registered_subject__subject_identifier']

    list_display = [
        'subject_visit',
        'report_datetime',
        'dashboard',
        'subject_referred',
        'referral_code',
        'referral_appt_date',
        'exported',
        'exported_datetime',
        'in_clinic_flag',
        ]

    list_filter = ['exported', 'in_clinic_flag', SubjectReferralIsReferredListFilter, SubjectCommunityListFilter, 'referral_code', 'report_datetime', 'referral_appt_date', 'exported_datetime', 'hostname_created']

    fields = (
        'subject_visit',
        'report_datetime',
        'subject_referred',
        'referral_code',
        'referral_appt_date',
        'referral_clinic',
        'comment'
        )

    radio_fields = {
        "referral_code": admin.VERTICAL,
        "referral_clinic": admin.VERTICAL,
        "subject_referred": admin.VERTICAL,
        }

    def get_actions(self, request):
        actions = super(SubjectReferralAdmin, self).get_actions(request)
        actions['export_as_csv_action'] = (  # This is a django SortedDict (function, name, short_description)
            export_as_csv_action(
                exclude=['exported', 'exported_datetime', self.visit_model_foreign_key, 'revision', 'hostname_created', 'hostname_modified', 'created', 'modified', 'user_created', 'user_modified', 'comment'],
                extra_fields=OrderedDict(
                    {'subject_identifier': self.visit_model_foreign_key + '__appointment__registered_subject__subject_identifier',
                     'first_name': self.visit_model_foreign_key + '__appointment__registered_subject__first_name',
                     'last_name': self.visit_model_foreign_key + '__appointment__registered_subject__last_name',
                     'initials': self.visit_model_foreign_key + '__appointment__registered_subject__initials',
                     'dob': self.visit_model_foreign_key + '__appointment__registered_subject__dob',
                     'identity': self.visit_model_foreign_key + '__appointment__registered_subject__identity',
                     'identity_type': self.visit_model_foreign_key + '__appointment__registered_subject__identity_type',
                     })
                ),
                'export_as_csv_action',
                "Export Referrals to CSV")
        actions['export_as_pipe_action'] = (  # This is a django SortedDict (function, name, short_description)
            export_as_csv_action(
                delimiter='|',
                encrypt=False,
                strip=True,
                exclude=[
                        'exported',
                        'revision',
                        'comment',
                        'in_clinic_flag',
                        'intend_residency',
                        'permanent_resident',
                        'direct_hiv_documentation',
                        'indirect_hiv_documentation',
                        'last_hiv_test_date',
                        'last_hiv_result',
                        'verbal_hiv_result',
                        'referral_clinic_other',
                        'exported',
                        'revision',
                        'hostname_created',
                        'hostname_modified',
                        'user_created',
                        'user_modified',
                        'created',
                        'modified',
                        'subject_visit'
                        ],
                extra_fields=OrderedDict(
                    {'subject_identifier': self.visit_model_foreign_key + '__appointment__registered_subject__subject_identifier',
                     'first_name': self.visit_model_foreign_key + '__appointment__registered_subject__first_name',
                     'last_name': self.visit_model_foreign_key + '__appointment__registered_subject__last_name',
                     'initials': self.visit_model_foreign_key + '__appointment__registered_subject__initials',
                     'dob': self.visit_model_foreign_key + '__appointment__registered_subject__dob',
                     'identity': self.visit_model_foreign_key + '__appointment__registered_subject__identity',
                     'identity_type': self.visit_model_foreign_key + '__appointment__registered_subject__identity_type',
                     })
                ),
                'export_as_pipe_action',
                "Export Referrals to Pipe (|) delimited file")
        return actions

admin.site.register(SubjectReferral, SubjectReferralAdmin)
