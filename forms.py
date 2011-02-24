#from django import forms


class BaseSubjectConsentForm(forms.ModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data 

        my_gender = cleaned_data.get("gender")
           
        """
        check omang if identity_type is omang
        """                        
        if cleaned_data.get("identity_type") == 'OMANG':
            check_omang_field(cleaned_data.get("identity"), my_gender)            
            
        """
        check 1st and last letters of initials match subjects name
        """
        my_first_name = cleaned_data.get("first_name") 
        my_last_name = cleaned_data.get("last_name") 
        my_initials = cleaned_data.get("initials") 
        check_initials_field(my_first_name, my_last_name, my_initials)
            

        # Always return the full collection of cleaned data.
        return cleaned_data    
    
    class Meta:
        abstract = True

