from django import forms

class OffStudyForm (forms.ModelForm):
    
    def clean(self):
        cleaned_data = self.cleaned_data 
        
        #check if StudyDrugInitiation <> None
        
        # Always return the full collection of cleaned data.
        return cleaned_data   

    
    class Meta:
        model = OffStudy

