from django import forms


class LocalResultForm(forms.ModelForm):

    def clean(self):
    
        cleaned_data = self.cleaned_data 
    
        return cleaned_data

class LocalResultItemForm(forms.ModelForm):

    def clean(self):
    
        cleaned_data = self.cleaned_data 
    
        return cleaned_data

class ReviewForm(forms.ModelForm):

    def clean(self):
    
        cleaned_data = self.cleaned_data 
    
        return cleaned_data

