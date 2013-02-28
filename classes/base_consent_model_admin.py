from django.contrib import admin
from bhp_crypto.admin import BaseCryptorModelAdmin
from bhp_consent.actions import flag_as_verified_against_paper, unflag_as_verified_against_paper


class BaseConsentModelAdmin(BaseCryptorModelAdmin):
    """Serves as the ModelAdmin for all consent models."""
    def __init__(self, *args, **kwargs):

        super(BaseConsentModelAdmin, self).__init__(*args, **kwargs)
        self.search_fields = ['id', 'subject_identifier', 'first_name', 'last_name', 'identity', ]
        self.list_display = ['subject_identifier', 'is_verified', 'first_name', 'initials', 'gender', 'dob',
                             'consent_datetime', 'created', 'modified', 'user_created', 'user_modified', ]
        self.actions.append(flag_as_verified_against_paper)
        self.actions.append(unflag_as_verified_against_paper)
        self.list_filter = [
            'gender',
            'is_verified',
            'may_store_samples',
            'study_site',
            'consent_datetime',
            'created',
            'modified',
            'user_created',
            'user_modified',
            'hostname_created']

    #override to disallow subject to be changed
    def get_readonly_fields(self, request, obj=None):

        super(BaseConsentModelAdmin, self).get_readonly_fields(request, obj)

        if obj:  # In edit mode
            return (
                'subject_identifier',
                #'first_name',
                #'last_name',
                'study_site',
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
        'confirm_identity',
        'is_incarcerated',
        'may_store_samples',
        'comment']
    radio_fields = {
        "gender": admin.VERTICAL,
        "study_site": admin.VERTICAL,
        "is_dob_estimated": admin.VERTICAL,
        "identity_type": admin.VERTICAL,
        "is_incarcerated": admin.VERTICAL,
        "may_store_samples": admin.VERTICAL}


class SubjectConsentAdminBase(BaseConsentModelAdmin):
    pass
