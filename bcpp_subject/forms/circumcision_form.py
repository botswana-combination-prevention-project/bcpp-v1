from django import forms
from bcpp_subject.models import Circumcision, Uncircumcised, Circumcised
from base_subject_model_form import BaseSubjectModelForm


class CircumcisionForm (BaseSubjectModelForm):

    class Meta:
        model = Circumcision


class CircumcisedForm (BaseSubjectModelForm):

    def clean(self):

        cleaned_data = super(CircumcisedForm, self).clean()
        if cleaned_data.get('circumcised') == 'Yes' and not cleaned_data.get('health_benefits_smc'):
            raise forms.ValidationError('if \'YES\', what are the benefits of male circumcision?.')

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
