from django import forms

class MyModelForm(forms.ModelForm):

    def clean(self):
    
        cleaned_data = self.cleaned_data 

        other =[]
        [other.append(k) for k in cleaned_data.iterkeys() if cleaned_data[k] == 'OTHER']
        for k in other:
            if k+'_other' in cleaned_data:
                if not cleaned_data[k+'_other']:        
                    raise forms.ValidationError("If %s is 'OTHER', please specify. You wrote '%s'" %  (k,cleaned_data[k+'_other']))

        super(MyModelForm, self).clean()
    
        return cleaned_data
        
    def validate_m2m(self, **kwargs):
    
        """Validate at form level a triplet of questions lead by a Yes/No for a many to many with other specify.
        
        The first question is a Yes/No question indicating if any items in the many to many will be selected
        The second question is a many to many (select all that apply)
        The third is an 'Other Specify' to be completed if an 'Other' item was selected in the many to many question

        Be sure to check cleaned_data for the 'key' of the m2m field first.
        
        For example, in the ModelForm clean() method call:

        if cleaned_data.has_key('chronic_cond'):
            self.validate_m2m(
                    label = 'chronic condition',
                    yesno = cleaned_data['has_chronic_cond'],
                    m2m = cleaned_data['chronic_cond'],
                    other = cleaned_data['chronic_cond_other'],
                )

        """
        
        label = kwargs.get('label', 'items to be selected')
        yesno = kwargs.get('yesno')
        m2m = kwargs.get('m2m')
        other = kwargs.get('other')
        
        # if lead question is 'Yes', a m2m item cannot be 'Not applicable'
        if yesno.lower() == 'yes' and [True for item in m2m if item.name.lower() == 'not applicable']:
            raise forms.ValidationError("You stated there ARE " + label + "s, yet you selected '%s'" %  item.name)        

        # if lead question is 'No', ensure the m2m item is 'not applicable'
        if yesno.lower() == 'no' and not [True for item in m2m if item.name.lower() == 'not applicable']:
           raise forms.ValidationError("You stated there are NO " + label + "s. Please correct")                

        # if lead question is 'No', ensure only one m2m item is selected.
        if yesno.lower() == 'no' and len(m2m) > 1:
            raise forms.ValidationError("You stated there are NO " + label + "s. Please correct")                

        # if lead question is 'Yes' and an m2m item is 'other, specify', ensure 'other' attribute has a value
        if yesno.lower() == 'yes' and not other and [True for item in m2m if item.name.lower() == 'other, specify']:        
            raise forms.ValidationError("You have selected a '" + label + "' as 'Other', please specify.")

        # if 'other' has a value but no m2m item is 'Other, specify'
        if other and not [True for item in m2m if item.name.lower() == 'other, specify']:
            raise forms.ValidationError("You have specified an 'Other' " + label + " but not selected 'Other, specify'. Please correct.")        

