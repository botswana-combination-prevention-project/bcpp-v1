
class LogicCheck(object):

    def test(self, cleaned_data, conditional_field, conditional_value, optional_field, logic='required_if_value'):
    
        self.cleaned_data = cleaned_data    
        self.conditional_field = conditional_field
        self.conditional_value = conditional_value
        self.optional_field - optional_field
        self.logic = logic

        if logic == 'required_if_value':
            """ if conditional_field == conditional_value ? required : not required """ 
            if self.cleaned_data.get(conditional_field).lower() == conditional_value and not self.cleaned_data.get(optional_field): 
                raise forms.ValidationError('%s is required.' % (optional_field,))
            if not self.cleaned_data.get(conditional_field).lower() == conditional_value and self.cleaned_data.get(optional_field): 
                raise forms.ValidationError('%s is not required if %s is %s. Please correct' % (optional_field, conditional_field, conditional_value,))
    
        if logic == 'not_required_if_value':
            """ if conditional_field == conditional_value ? not required : required """     
            if self.cleaned_data.get(conditional_field).lower() == conditional_value and self.cleaned_data.get(optional_field): 
                raise forms.ValidationError('%s is not required if %s is %s. Please correct' % (optional_field, conditional_field, conditional_value,))
            if not self.cleaned_data.get(conditional_field).lower() == conditional_value and not self.cleaned_data.get(optional_field): 
                raise forms.ValidationError('%s is required.' % (optional_field,))
    
