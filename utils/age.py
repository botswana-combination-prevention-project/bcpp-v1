from datetime import *
from dateutil.relativedelta import *

def formatted_age(born, reference_date, month_lower_boundry=0):

    """
        if month_lower_boundry = 0, first month will ready as 1m, etc
        if month_lower_boundry = 1, first month will ready as 
        30/31/28/29 days and second month will be 2mxd  
    """
    
    if born:
        rdelta = relativedelta(reference_date, born)
        if born > reference_date:
            return '?'
        elif rdelta.years == 0 and rdelta.months <= month_boundry:
            return '%sd' % (rdelta.days)
        elif rdelta.years == 0 and rdelta.months > month_boundry and rdelta.months <= 2:
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
