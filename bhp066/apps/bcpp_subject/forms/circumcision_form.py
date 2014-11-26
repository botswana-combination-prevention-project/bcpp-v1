from django import forms

from apps.bcpp_survey.models import Survey

from ..models import Circumcision, Uncircumcised, Circumcised

from .base_subject_model_form import BaseSubjectModelForm


class CircumcisionForm (BaseSubjectModelForm):

    def __init__(self, *args, **kwargs):
        super(CircumcisionForm, self).__init__(*args, **kwargs)
        # customize for annual surveys
        if Survey.objects.current_survey().survey_slug != Survey.objects.first_survey.survey_slug:
            self.fields['circumcised'].label = (
                'Have you been circumcised since we last spoke with you?')

    class Meta:
        model = Circumcision


class CircumcisedForm (BaseSubjectModelForm):

    def clean(self):

        cleaned_data = super(CircumcisedForm, self).clean()
        if cleaned_data.get('circumcised') == 'Yes' and not cleaned_data.get('health_benefits_smc'):
            raise forms.ValidationError('if \'YES\', what are the benefits of male circumcision?.')
        if cleaned_data.get('when_circ') and not cleaned_data.get('age_unit_circ'):
            raise forms.ValidationError('If you answered age of circumcision then you must provide time units.')
        if not cleaned_data.get('when_circ') and cleaned_data.get('age_unit_circ'):
            raise forms.ValidationError(
                'If you did not answer age of circumcision then you must not provide time units.')
        return cleaned_data

    class Meta:
        model = Circumcised


class UncircumcisedForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = super(UncircumcisedForm, self).clean()
        if cleaned_data.get('circumcised') == 'Yes' and not cleaned_data.get('health_benefits_smc'):
            raise forms.ValidationError('if \'YES\', what are the benefits of male circumcision?.')
        return cleaned_data

    class Meta:
        model = Uncircumcised
