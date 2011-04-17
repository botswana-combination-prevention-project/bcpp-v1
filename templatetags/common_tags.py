from datetime import *
from dateutil.relativedelta import *
from django import template

register = template.Library()

@register.filter(name='age')
def age(born):
    today = date.today()
    rdelta = relativedelta(today, born)
    if born > today:
        return '?'
    elif rdelta.years == 0 and rdelta.months == 0:
        return '%sd' % (rdelta.days)
    elif rdelta.years == 0 and rdelta.months > 0 and rdelta.months <= 2:
        return '%sm%sd' % (rdelta.months,rdelta.days)
    elif rdelta.years == 0 and rdelta.months > 2:
        return '%sm' % (rdelta.months)
    elif rdelta.years == 1: 
        m = rdelta.months + 12
        return '%sm' % (m)        
    elif rdelta.years > 1:
        return '%sy' % (rdelta.years)
    else:
         raise TypeError('Age template tag missed a case... today - born. redelta = %s and %s' % (rdelta, born))   

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

