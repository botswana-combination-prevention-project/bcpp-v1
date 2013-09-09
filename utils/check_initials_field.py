from django import forms
from django.core.exceptions import ValidationError

def check_initials_field(first_name, last_name, initials):
    """
        check that the first and last initials match what is expected based on 
        first and last name
        
    """
    if initials != None and first_name != None:
        if first_name[:1].upper() != initials[:1].upper():
            raise forms.ValidationError("First initial does not match first name, expected '%s' but you wrote %s." % (first_name[:1], initials[:1]))
            
    if initials != None and last_name != None:
        if last_name[:1].upper() != initials[-1:].upper():
            raise forms.ValidationError("Last initial does not match last name, expected '%s' but you wrote %s." % (last_name[:1], initials[-1:]))

