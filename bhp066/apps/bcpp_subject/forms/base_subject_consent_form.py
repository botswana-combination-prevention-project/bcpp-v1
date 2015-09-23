from datetime import date
from dateutil.relativedelta import relativedelta
from django import forms

from edc.core.bhp_common.utils import formatted_age
from bhp066.apps.bcpp.base_model_form import BaseModelForm


class BaseSubjectConsentForm(BaseModelForm):
    """Form for models that are a subclass of BaseConsent."""
    def clean(self):

        cleaned_data = self.cleaned_data

        if not cleaned_data.get("gender", None):
            raise forms.ValidationError('Please specify the gender')
        for field in self._meta.model._meta.fields:
            try:
                field.validate_with_cleaned_data(field.attname, cleaned_data)
            except AttributeError:
                pass
        if cleaned_data.get('consent_datetime', None):
            consent_datetime = cleaned_data.get('consent_datetime').date()
        else:
            consent_datetime = date.today()
        if cleaned_data.get('dob', None):
            rdelta = relativedelta(consent_datetime, cleaned_data.get('dob'))
            if rdelta.years < self._meta.model.Constants.MIN_AGE_OF_CONSENT:
                raise forms.ValidationError(
                    'Subject\'s age is {}. Subject is not eligible for consent.'.format(
                        formatted_age(cleaned_data.get('dob'), date.today())))
            if rdelta.years > self._meta.model.Constants.MAX_AGE_OF_CONSENT:
                raise forms.ValidationError(
                    'Subject\'s age is {}. Subject is not eligible for consent.'.format(
                        formatted_age(cleaned_data.get('dob'), date.today())))
            if rdelta.years < self._meta.model.Constants.AGE_IS_ADULT:
                if "guardian_name" not in cleaned_data.keys():
                    raise forms.ValidationError(
                        'Subject is a minor. "guardian_name" is required but missing from the form. '
                        'Please add this field to the form.')
                elif not cleaned_data.get("guardian_name", None):
                    raise forms.ValidationError(
                        'Subject\'s age is {}. Subject is a minor. Guardian\'s '
                        'name is required here and with signature on the paper document.'.format(
                            formatted_age(cleaned_data.get('dob'), date.today())))
                else:
                    pass
            if rdelta.years >= self._meta.model.Constants.AGE_IS_ADULT and "guardian_name" in cleaned_data.keys():
                if not cleaned_data.get("guardian_name", None) == '':
                    raise forms.ValidationError(
                        'Subject\'s age is {}. Subject is an adult. Guardian\'s name is '
                        'NOT required.'.format(formatted_age(cleaned_data.get('dob'), date.today())))
        if hasattr(self._meta.model, 'ConsentAge'):
            instance = self._meta.model()
            consent_age_range = instance.ConsentAge()
            rdelta = relativedelta(consent_datetime, cleaned_data.get('dob'))
            if rdelta.years not in consent_age_range:
                raise forms.ValidationError(
                    "Invalid Date of Birth. Age of consent must be between {}y and {}y"
                    " inclusive. Got {}y".format(consent_age_range[0], consent_age_range[-1], rdelta.years,))

        # check for gender of consent
        if cleaned_data.get('gender'):
            if cleaned_data.get('gender') not in self._meta.model.Constants.GENDER_OF_CONSENT:
                raise forms.ValidationError(
                    'Expected gender to be one of {}. Got {}.'.format(
                        self._meta.model.Constants.GENDER_OF_CONSENT, cleaned_data.get('gender')))
        # confirm attr identity and confirm_identity match
        if cleaned_data.get('identity') and cleaned_data.get('confirm_identity'):
            if cleaned_data.get('identity') != cleaned_data.get('confirm_identity'):
                raise forms.ValidationError('Identity mismatch. Identity number must match the confirmation field.')
        # consent cannot be submitted if answer is none to last four consent questions
        if not cleaned_data.get('consent_reviewed', None) or cleaned_data.get('consent_reviewed', None) == 'No':
            raise forms.ValidationError('If consent reviewed is No, patient cannot be enrolled')
        if not cleaned_data.get('study_questions', None) or cleaned_data.get('study_questions', None) == 'No':
            raise forms.ValidationError('If unable to answer questions from client and/or None, patient cannot be enrolled')
        if 'assessment_score' in cleaned_data:
            if not cleaned_data.get('assessment_score', None) or cleaned_data.get('assessment_score', None) == 'No':
                raise forms.ValidationError('Client assessment should at least be a passing score. If No, patient cannot be enrolled')
        if not self.accepted_consent_copy(cleaned_data):
            raise forms.ValidationError('If patient has not been given consent copy and/or None, patient cannot be enrolled')

        if cleaned_data.get('is_literate', None) == 'No' and not cleaned_data.get('witness_name', None):
            raise forms.ValidationError('You wrote subject is illiterate. Please provide the name of a witness here and with signature on the paper document.')
        if cleaned_data.get('is_literate') == 'Yes' and cleaned_data.get('witness_name', None):
            raise forms.ValidationError('You wrote subject is literate. The name of a witness is NOT required.')
        # Always return the full collection of cleaned data.
        return super(BaseSubjectConsentForm, self).clean()

    def accepted_consent_copy(self, cleaned_data):
        if not cleaned_data.get('consent_copy', None) or cleaned_data.get('consent_copy', None) == 'No':
            return False
        else:
            return True
