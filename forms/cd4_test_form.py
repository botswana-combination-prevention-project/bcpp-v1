from django import forms
from base_htc_model_form import BaseHtcModelForm
from bcpp_htc.models import CD4Test


class CD4TestForm (BaseHtcModelForm):
    
    def clean(self):
        cleaned_data=super(CD4TestForm)
        cd4_result=cleaned_data("cd4_result")
        referral_clinic=cleaned_data("referral_clinic")
        appointment_date=cleaned_data("appointment_date")
        
        if cd4_result|referral_clinic|appointment_date is None:
            raise forms.ValidationError("Please fill in all the fields below")
        
        return cleaned_data
    
    class Meta:
        model = CD4Test