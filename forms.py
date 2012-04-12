from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from django import forms
from bhp_variables.models import StudySpecific
from bhp_common.utils import check_omang_field, check_initials_field, formatted_age


class BaseSubjectConsentForm(forms.ModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data 

        """
        check omang if identity_type is omang
        """                        
        if cleaned_data.get("identity_type", None) == 'OMANG':
            check_omang_field(cleaned_data["identity"], cleaned_data["gender"])            
    
        if 'subject_identifier' in cleaned_data: #which it never is??
            consents = self._meta.model.objects.filter(identity=cleaned_data["identity"]).exclude(subject_identifier=cleaned_data["subject_identifier"])
        else:
            consents = self._meta.model.objects.filter(identity=cleaned_data["identity"])        
        if consents:
            consent = self._meta.model.objects.get(identity=cleaned_data["identity"])
            raise forms.ValidationError('Omang already on file for subject %s, %s (%s)' % (consent.last_name, consent.first_name, consent.subject_identifier))            
            
        """
        check 1st and last letters of initials match subjects name
        """
        my_first_name = cleaned_data.get("first_name") 
        my_last_name = cleaned_data.get("last_name") 
        my_initials = cleaned_data.get("initials")
        check_initials_field(my_first_name, my_last_name, my_initials)
            
        # obj=StudySpecific.objects.all()[0]
        # rdelta = relativedelta(datetime.today(), cleaned_data['dob']) 
        # don't need this check, is done at the field level...
        # if rdelta.years < obj.minimum_age_of_consent:
        #    raise forms.ValidationError('Subject\'s age is below age of consent of %s for this protocol. You wrote %s.' % (obj.minimum_age_of_consent, rdelta.years))

        """
        if minor, force specify guardian's name
        """
        obj=StudySpecific.objects.all()[0]
        if cleaned_data.get('dob'):
            rdelta = relativedelta(date.today(), cleaned_data.get('dob')) 
            if rdelta.years < obj.age_at_adult_lower_bound and cleaned_data["guardian_name"] == '':
                raise forms.ValidationError(u'Subject\'s age is %s. Subject is a minor. Guardian\'s name is required.' % (formatted_age(cleaned_data['dob'], date.today())))
            if rdelta.years >= obj.age_at_adult_lower_bound and not cleaned_data["guardian_name"] == '':
                raise forms.ValidationError(u'Subject\'s age is %s. Subject is an adult. Guardian\'s name is NOT required.' % (formatted_age(cleaned_data['dob'], date.today())))

        
        # if consent model has a ConsentAge method that returns an ordered range of ages as list
        if hasattr(self._meta.model, 'ConsentAge'):
            instance = self._meta.model()
            consent_age_range = instance.ConsentAge()
            rdelta = relativedelta(datetime.today(), cleaned_data.get('dob'))
            if rdelta.years not in consent_age_range:
                raise forms.ValidationError("Invalid Date of Birth. Age of consent must be between %sy and %sy inclusive. Got %sy" % (consent_age_range[0], consent_age_range[-1],rdelta.years,))
        
        # Always return the full collection of cleaned data.
        return cleaned_data    
    
        

