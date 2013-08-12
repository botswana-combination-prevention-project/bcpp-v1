from django import forms
from base_subject_model_form import BaseSubjectModelForm
from bcpp_subject.models import Demographics


class DemographicsForm (BaseSubjectModelForm):

    def clean(self):

        cleaned_data = super(DemographicsForm, self).clean()
        #validation religion
#         if cleaned_data.get('religion')[0].name == 'Other' and not cleaned_data.get('religion_other'):
#             raise forms.ValidationError('If participant\'s religion not in given list, name the religion')
#         #validation- ethnic group
#         if cleaned_data.get('ethnic')[0].name == 'Other, specify' and not cleaned_data.get('other'):
#             raise forms.ValidationError('If participant\'s ethnic group is not in the given list, name the ethnic group')
#         #validating marital status
        #asked if female
        if cleaned_data.get('marital_status') == 'Married' and not cleaned_data.get('num_wives'):
            raise forms.ValidationError('If participant is married, give number of wives')
        #asked if male
        if cleaned_data.get('marital_status') == 'Married' and not cleaned_data.get('husband_wives'):
            raise forms.ValidationError('If participant is married, how many wives is he married to, including traditional marriages?')
        return cleaned_data

    class Meta:
        model = Demographics
