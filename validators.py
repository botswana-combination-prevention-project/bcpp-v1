from datetime import datetime, date, timedelta
from django.core.exceptions import ValidationError


"""
check if decimal value of visit code is sequentially correct
"""
def IsNextVisitInstance (value):
    now  = date.today()
    if now == value :
        raise ValidationError(u'Date of birth cannot be today. You entered %s.' % value)


