from datetime import *
from dateutil.relativedelta import *
from django import template
from bhp_common.utils import formatted_age, round_up

register = template.Library()

@register.filter(name='age')
def age(born):
    reference_date = date.today()
    return formatted_age(born, reference_date)

@register.filter(name='dob_or_dob_estimated')
def dob_or_dob_estimated(dob, is_dob_estimated):
    if dob > date.today():
        return 'Unknown'
    elif is_dob_estimated.lower() == '-':
        return dob.strftime('%Y-%m-%d')
    elif is_dob_estimated.lower() == 'd':
        return dob.strftime('%Y-%m-XX')
    elif is_dob_estimated.lower() == 'md':
        return dob.strftime('%Y-XX-XX')
    else:
        return dob.strftime('%Y-%m-%d')


@register.filter(name='gender')
def gender(value):
    if value.lower() == 'f':
        return 'Female'
    elif value.lower() == 'm':
        return 'Male'
    elif value.lower() == '-1':
        return '?'
    elif value.lower() == '-9':
        return '?'
    else:
        return value    
        
        
@register.filter(name='roundup')
def roundup(d, digits):
    return round_up(d, digits)   



