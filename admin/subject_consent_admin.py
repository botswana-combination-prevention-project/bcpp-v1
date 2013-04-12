from django.contrib import admin
from bhp_consent.admin import BaseConsentModelAdmin
from bcpp_subject.models import SubjectConsent
from bcpp_subject.forms import SubjectConsentForm


# SubjectConsent
class SubjectConsentAdmin(BaseConsentModelAdmin):
    date_heirarchy = 'consent_datetime'
    form = SubjectConsentForm
    fields = (
        "subject_identifier",
        "first_name",
        "last_name",
        "initials",
        "consent_datetime",
        "gender",
        "study_site",
        "guardian_name",
        "dob",
        "is_dob_estimated",
        "identity",
        "identity_type",
        "confirm_identity",
        "may_store_samples",
        "is_incarcerated",
        "comment",
        "consent_reviewed",
        "study_questions",
        "assessment_score",
        "consent_copy")
    radio_fields = {
        "study_site": admin.VERTICAL,
        "identity_type": admin.VERTICAL,
        "may_store_samples": admin.VERTICAL,
        "gender": admin.VERTICAL,
        "is_dob_estimated": admin.VERTICAL,
        "is_incarcerated": admin.VERTICAL, 
        "consent_reviewed": admin.VERTICAL,
        "study_questions": admin.VERTICAL,
        "assessment_score": admin.VERTICAL,
        "consent_copy": admin.VERTICAL}
    readonly_fields = ('subject_identifier',)

admin.site.register(SubjectConsent, SubjectConsentAdmin)
