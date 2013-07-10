from django import forms
from bhp_base_form.forms import BaseModelForm
from bcpp_subject.models import SubjectConsent  # SubjectConsentYearOne, SubjectConsentYearTwo, SubjectConsentYearThree, SubjectConsentYearFour, SubjectConsentYearFive


class BaseMembershipForm(BaseModelForm):

    #subject_consent_model_cls = {'bcpp-year-1': SubjectConsentYearOne, 'bcpp-year-2': SubjectConsentYearTwo, 'bcpp-year-3': SubjectConsentYearThree, 'bcpp-year-4': SubjectConsentYearFour, 'bcpp-year-5': SubjectConsentYearFive}

    def clean(self):

        cleaned_data = self.cleaned_data
        if cleaned_data:
            # do not allow any membership forms to go in if subject is already consented for this survey
            household_member = cleaned_data.get('household_member', None)
            if not household_member:
                household_member = cleaned_data.get(self.household_member_fk, None).household_member
            if not household_member:
                raise forms.ValidationError('Unable to determine the household structure member for this instance.')
            subject_consent_model_cls = SubjectConsent.objects.get(household_member.survey.survey_slug)
            subject_consent = subject_consent_model_cls.objects.filter(household_member=household_member)
            if subject_consent:
                subject_consent = SubjectConsent.objects.get(household_member=household_member)
                if cleaned_data.get('report_datetime', None) > subject_consent.consent_datetime:
                    raise forms.ValidationError("Report may not be submitted for survey {}. Subject is already consented for this survey.".format(subject_consent.survey.survey_name,))

        return super(BaseMembershipForm, self).clean()
