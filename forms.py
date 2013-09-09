from django import forms
from bhp_base_form.forms import BaseModelForm


class BaseRequisitionForm (BaseModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        if cleaned_data['is_drawn'].lower() == 'yes' and not cleaned_data['drawn_datetime']:
            raise forms.ValidationError("Date and Time Drawn must be provided if a sample was drawn.")
        if cleaned_data['is_drawn'].lower() == 'no' and cleaned_data['drawn_datetime']:
            raise forms.ValidationError("You have indicated a Date and Time Drawn but no sample was drawn. Please correct.")
        if cleaned_data['is_drawn'].lower() == 'no' and not cleaned_data['reason_not_drawn']:
            raise forms.ValidationError("Please provide a reason why sample was not drawn.")
        if cleaned_data['is_drawn'].lower() == 'yes' and cleaned_data['reason_not_drawn']:
            raise forms.ValidationError("You have provided a reason why sample was not drawn yet indicate that it was drawn. Please correct.")
        return cleaned_data
