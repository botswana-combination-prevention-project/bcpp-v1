from django.contrib import admin
from bhp_crypto.classes import BaseCryptorModelAdmin as BaseModelAdmin


class BaseSubjectConsentAdmin(BaseModelAdmin):

    def __init__(self, *args, **kwargs):

        super(BaseSubjectConsentAdmin, self).__init__(*args, **kwargs)
        self.search_fields = ['id', 'subject_identifier', 'first_name', 'last_name', 'identity', ]
        self.list_display = ['subject_identifier', 'first_name', 'initials', 'gender', 'dob',
                             'consent_datetime', 'created', 'modified', 'user_created', 'user_modified', ]

        self.list_filter = [
            'gender',
            'study_site',
            'consent_datetime',
            'created',
            'modified',
            'user_created',
            'user_modified',
            'hostname_created',
            ]

    #override to disallow subject to be changed
    def get_readonly_fields(self, request, obj=None):

        super(BaseSubjectConsentAdmin, self).get_readonly_fields(request, obj)

        if obj:  # In edit mode
            return (
                'subject_identifier',
                'first_name',
                'last_name',
                'study_site',
                #'initials',
                'consent_datetime',) + self.readonly_fields
        else:
            return ('subject_identifier',) + self.readonly_fields

    fields = [
        'subject_identifier',
        'first_name',
        'last_name',
        'initials',
        'consent_datetime',
        'study_site',
        'gender',
        'dob',
        'is_dob_estimated',
        'identity',
        'identity_type',
        #'guardian_name',
        'may_store_samples',
        'comment',
        ]
    radio_fields = {
        "gender": admin.VERTICAL,
        "study_site": admin.VERTICAL,
        "is_dob_estimated": admin.VERTICAL,
        "identity_type": admin.VERTICAL,
        "may_store_samples": admin.VERTICAL,
        }


class SubjectConsentAdminBase(BaseSubjectConsentAdmin):
    pass
