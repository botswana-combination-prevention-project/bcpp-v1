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
        
    def validate_m2m(self, **kwargs ):
    
        """Validate at form level a triplet of questions lead by a Yes/No for a many to many with other specify.
        
        The first question is a Yes/No question indicating if any items in the many to many will be selected
        The second question is a many to many (select all that apply)
        The third is an 'Other Specify' to be completed if an 'Other' item was selected in the many to many question

        Be sure to cleaned_data for the 'key' of the m2m field first.
        
        For example, in the clean method call:

        if cleaned_data.has_key('chronic_cond'):
            self.validate_m2m(
                    label = 'chronic condition',
                    yesno = cleaned_data['has_chronic_cond'],
                    m2m = cleaned_data['chronic_cond'],
                    other = cleaned_data['chronic_cond_other'],
                )

        """
        
        label = kwargs.get('label')
        yesno = kwargs.get('yesno')
        m2m = kwargs.get('m2m')
        other = kwargs.get('other')
        
        if yesno.lower() == 'yes':
            for cond in m2m: 
                if cond.name.lower() == 'not applicable':
                    raise forms.ValidationError("The participant has " + label + ". You wrote '%s'" %  cond.name)        

        # if yesno == No => only one item in list and item must be 'not applicable'
        if yesno.lower() == 'no':
            found = [True for cond in m2m if cond.name.lower() == 'not applicable']
            if not found:
               raise forms.ValidationError("The participant has NO " + label + ". Please correct")                

        if yesno.lower() == 'no' and len(m2m) > 1:
            raise forms.ValidationError("The participant has NO " + label + ". Please correct")                

        """if m2m == 'other, specify', other may not be blank"""           
        if yesno.lower() == 'yes':        
            for cond in m2m: 
                if cond.name.lower() == 'other, specify' and not other:
                    raise forms.ValidationError("If " + label + " is 'Other', please specify.")
        
        if other:
            found = [True for cond in m2m if cond.name.lower() == 'other, specify']
            if not found:
                raise forms.ValidationError("You have specified an 'Other' condition but not selected 'Other, specify'. Please correct.")        

