from django import forms
from bhp_variables.models import StudySpecific
from bhp_common.utils import check_omang_field, check_initials_field



class BaseSubjectConsentForm(forms.ModelForm):

#class BaseSubjectConsentForm(forms.ModelForm):

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
            
        """
        if minor, force specify guardian's name
        """
        obj=StudySpecific.objects.all()[0]
        if cleaned_data.get("age_in_years") < obj.age_at_adult_lower_bound and cleaned_data.get("guardian_name") == '':
            raise ValidationError(_(u'Subject\'s age is %s. Subject is a minor. Guardian\'s name is required.') % (  cleaned_data.get("age_in_years") ))

        # Always return the full collection of cleaned data.
        return cleaned_data    
    
    class Meta:
        abstract = True
        
        

