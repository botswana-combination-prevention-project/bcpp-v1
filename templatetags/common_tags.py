from datetime import *
from dateutil.relativedelta import *
from django import template

register = template.Library()

@register.filter(name='age')
def age(born):
    today = date.today()
    rdelta = relativedelta(today, born)
    if rdelta.years == 0 and rdelta.months == 0:
        return '%sd' % (rdelta.days,'d')
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
         raise TypeError('Age template tag missed a case... today - born. redelta = %s' % (rdelta))   


@register.filter(name='gender')
def gender(value):
    if value.lower() == 'f':
        return 'Female'
    elif value.lower() == 'm':
        return 'Male'
    else:
        return value    

