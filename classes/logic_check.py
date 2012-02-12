from django import forms


class LogicCheck(object):

    def __init__(self, model):
        
        self.model = model

    def test(self, cleaned_data, conditional_field, condition_value, optional_field, logic='required_if_value', required_optional_field_value = None):
    
        conditional_field_value = cleaned_data.get(conditional_field, None)
        if isinstance(conditional_field_value, basestring):
            conditional_field_value = conditional_field_value.lower()    
        conditional_field_verbose_name = [field.verbose_name for field in self.model._meta.fields if field.name==conditional_field][0]
                        
        if isinstance(condition_value, basestring):
            condition_value = condition_value.lower()    

        optional_field_value = cleaned_data.get(optional_field, None)
        if isinstance(optional_field_value, basestring):
            optional_field_value = optional_field_value.lower()    
        optional_field_verbose_name = [field.verbose_name for field in self.model._meta.fields if field.name==optional_field][0]

        if logic == 'required_if_value':
            """ if conditional_field == condition_value ? required : not required """ 
            if conditional_field_value:
                if conditional_field_value == condition_value and not optional_field_value: 
                    raise forms.ValidationError('Please provide an answer for \'%s\'...' % (optional_field_verbose_name,))
                if not conditional_field_value == condition_value and optional_field_value: 
                    raise forms.ValidationError('%s is not required if %s is %s. Please correct' % (optional_field, conditional_field, condition_value,))
    
        if logic == 'not_required_if_value':
            """ if conditional_field == condition_value ? not required : required """     
            if conditional_field_value:
                if conditional_field_value == condition_value and optional_field_value: 
                    raise forms.ValidationError('%s is not required if %s is %s. Please correct' % (optional_field, conditional_field, condition_value,))
                if not conditional_field_value == condition_value and not optional_field_value: 
                    raise forms.ValidationError('Please provide an answer for \'%s\'...' % (optional_field_verbose_name,))
    
    
        if logic == 'if_condition_then':
            if conditional_field_value:
                if conditional_field_value == condition_value and not optional_field_value == required_optional_field_value: 
                    raise forms.ValidationError('%s must be %s if %s is %s. Please correct' % (optional_field, required_optional_field_value, conditional_field, condition_value,))
                if not conditional_field_value == condition_value and optional_field_value == required_optional_field_value: 
                    raise forms.ValidationError('%s cannot be %s if %s is %s. Please correct' % (optional_field, optional_field_value, conditional_field, condition_value,))

