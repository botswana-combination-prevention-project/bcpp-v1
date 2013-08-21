from django import forms
from base_htc_model_form import BaseHtcModelForm
from bcpp_htc.models import HivResult


class HivResultForm (BaseHtcModelForm):
    
    def clean(self):
        cleaned_data=super(HivResultForm).clean()
        couples_testing=cleaned_data.get("couples_testing")
        partner_id=cleaned_data.get("partner_id")
        
        if couples_testing == 'Yes' and partner_id is None:
            raise forms.ValidationError("Partner unique identifier required.")
        
        return cleaned_data           
        
    class Meta:
        model = HivResult