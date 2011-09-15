from django import forms
from lab_clinic_api.models import Review

class LabForm(forms.ModelForm):

    def clean(self):
    
        cleaned_data = self.cleaned_data 
    
        return cleaned_data


class ResultForm(forms.ModelForm):

    def clean(self):
    
        cleaned_data = self.cleaned_data 
    
        return cleaned_data

class ResultItemForm(forms.ModelForm):

    def clean(self):
    
        cleaned_data = self.cleaned_data 
    
        return cleaned_data

class ReviewForm(forms.ModelForm):

    def clean(self):
    
        cleaned_data = self.cleaned_data 
    
        return cleaned_data


class ResultSearchForm(forms.Form):

    result_search_term = forms.CharField(
        max_length=35, 
        label="Search term",
        help_text="enter all or part of a order number, sample identifier, patient identifier, etc",
        error_messages={'required': 'Please enter a search term.'},
        )

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review

