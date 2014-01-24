from django.contrib import admin
from edc.subject.consent.admin import BaseConsentModelAdmin
from ..models import ClinicConsent
from ..forms import ClinicConsentForm


class ClinicConsentAdmin(BaseConsentModelAdmin):

    dashboard_type = 'clinic'
    form = ClinicConsentForm

    def __init__(self, *args, **kwargs):
        super(ClinicConsentAdmin, self).__init__(*args, **kwargs)
        for i, item in enumerate(self.fields):
            if item == 'assessment_score':
                del self.fields[i]

        self.list_filter = [
            'gender',
            'is_verified',
            'language',
            'may_store_samples',
            'is_literate',
            'consent_datetime',
            'community',
            'created',
            'modified',
            'user_created',
            'user_modified',
            'hostname_created']

        self.fields = [
            'subject_identifier',
            'first_name',
            'last_name',
            'initials',
            'language',
            'is_literate',
            'witness_name',
            'consent_datetime',
            'gender',
            'dob',
            'guardian_name',
            'is_dob_estimated',
            'identity',
            'identity_type',
            'confirm_identity',
            'may_store_samples',
            'comment',
            'consent_reviewed',
            'study_questions',
            'assessment_score',
            'consent_signature',
            'consent_copy']

        self.radio_fields = {
            "language": admin.VERTICAL,
            "gender": admin.VERTICAL,
            "is_dob_estimated": admin.VERTICAL,
            "identity_type": admin.VERTICAL,
            "may_store_samples": admin.VERTICAL,
            "consent_reviewed": admin.VERTICAL,
            "study_questions": admin.VERTICAL,
            "assessment_score": admin.VERTICAL,
            'consent_signature': admin.VERTICAL,
            "consent_copy": admin.VERTICAL,
            "is_literate": admin.VERTICAL}

        self.radio_fields.update({"is_minor": admin.VERTICAL})

admin.site.register(ClinicConsent, ClinicConsentAdmin)
