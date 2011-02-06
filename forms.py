from django import forms
from bhp_consent.models import SubjectConsent


class SubjectConsentForm(forms.ModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data 

        if cleaned_data.get("gender") != 'F':
            raise forms.ValidationError("Gender must be FEMALE. Please correct and try saving again." )

        # Always return the full collection of cleaned data.
        return cleaned_data    
    
    class Meta:
        model = SubjectConsent   
