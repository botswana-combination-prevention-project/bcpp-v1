from django import forms
from base_subject_model_form import BaseSubjectModelForm
from bcpp_subject.models import Demographics


class DemographicsForm (BaseSubjectModelForm):

#     def clean(self):
# 
#         cleaned_data = super(DemographicsForm, self).clean()
#         #This will later be used under conditional fields. For now its commented out and help text is given on the model form
#         #asked if female
# #         if cleaned_data.get('marital_status') == 'Married' and not cleaned_data.get('num_wives'):
# #             raise forms.ValidationError('If participant is married, give number of wives')
#         #asked if male
# #         if cleaned_data.get('marital_status') == 'Married' and not cleaned_data.get('husband_wives'):
# #             raise forms.ValidationError('If participant is married, how many wives is he married to, including traditional marriages?')
#         return cleaned_data

    class Meta:
        model = Demographics
