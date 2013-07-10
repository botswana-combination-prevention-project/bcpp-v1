from django import forms
from base_subject_model_form import BaseSubjectModelForm
from bcpp_subject.models import Demographics


class DemographicsForm (BaseSubjectModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        #validating religion affiliation
        if cleaned_data.get('religion') == 'Christian' and not cleaned_data.get('religion_other'):
            raise forms.ValidationError('If participant is a Christian, specify denomination.')
        #validating Other
        if cleaned_data.get('ethnic') == 'Other' and not cleaned_data.get('other'):
            raise forms.ValidationError('If participant ethnic group not given in list-of-options, specify the ethnic group.')
        #validating marital status
        if cleaned_data.get('marital_status') == 'Married' and not cleaned_data.get('num_wives'):
            raise forms.ValidationError('If participant is married, give number of wives')
        cleaned_data = super(DemographicsForm, self).clean()
        return cleaned_data

    class Meta:
        model = Demographics
