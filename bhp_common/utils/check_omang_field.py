#import re
#from django.core.exceptions import ValidationError
            
def check_omang_field(omang, gender):            
    
    raise TypeError('check_omang_field() is deprecated as this field uses encryption. Use EncryptedField method validate_with_cleaned_data()')
    #    str_value = "%s" % (omang)
    #    pattern = ""
    #    if gender=='M':
    #        pattern = '^[0-9]{4}[1]{1}[0-9]{4}$'
    #    if gender=='F':
    #        pattern = '^[0-9]{4}[2]{1}[0-9]{4}$'        
    #
    #    if pattern:
    #        p = re.compile(pattern)
    #        if p.match(str_value) == None:
    #            raise ValidationError(u'Invalid Omang number for gender (%s). You entered %s.' % (gender, str_value))
    #            

    
    


