import re
from django.core.exceptions import ValidationError

def TelephoneNumber(value, pattern, word):
    str_value = "%s" % (value)
    p = re.compile(pattern)
    if p.match(str_value) == None:
        raise ValidationError(u'Invalid %s number. You entered %s.' % (word, str_value))
