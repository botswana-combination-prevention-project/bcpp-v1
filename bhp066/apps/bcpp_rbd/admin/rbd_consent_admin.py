from django.contrib import admin

from edc.subject.consent.admin import BaseConsentModelAdmin
from edc.subject.registration.models import RegisteredSubject

from apps.bcpp_household_member.models import HouseholdMember

from ..forms import RBDConsentForm
from ..models import RBDConsent


class RBDConsentAdmin(BaseConsentModelAdmin):

    dashboard_type = 'rbd_subject'
    form = RBDConsentForm

    def __init__(self, *args, **kwargs):
        super(RBDConsentAdmin, self).__init__(*args, **kwargs)
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
            'household_member',
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
            'consent_copy',
            'mentally_incapacitated',
            'involuntary_incarceration']

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
            "is_literate": admin.VERTICAL,
            "mentally_incapacitated": admin.VERTICAL,
            "involuntary_incarceration": admin.VERTICAL}

        self.search_fields.append('household_member__household_structure__household__household_identifier')
        self.search_fields.append('household_member__household_structure__household__plot__plot_identifier')
        self.radio_fields.update({"is_minor": admin.VERTICAL})

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_member":
            kwargs["queryset"] = HouseholdMember.objects.filter(id__exact=request.GET.get('household_member', 0))
        if db_field.name == "registered_subject":
            kwargs["queryset"] = RegisteredSubject.objects.filter(id__exact=request.GET.get('registered_subject', 0))
        return super(RBDConsentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(RBDConsent, RBDConsentAdmin)
