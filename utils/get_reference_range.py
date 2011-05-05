from bhp_common.utils import get_age_in_days
from bhp_lab_core.models import TestCodeReference

def get_reference_range(**kwargs):
    ref_range_value = ''
    #get age in days using the collection date as a reference
    age_in_days = get_age_in_days(kwargs.get('datetime_drawn'), kwargs.get('dob'))
    #filter for reference ranges for this testcode, gender
    oTestCodeReference = TestCodeReference.objects.filter(test_code=kwargs.get('test_code'), gender__icontains=kwargs.get('gender'))    
    #loop to find record for this age_in_days
    if oTestCodeReference:

        for reference in oTestCodeReference:
            #find the record for this age 
            if reference.age_low_days() <= age_in_days and reference.age_high_days() >= age_in_days:
                if kwargs.get('range_category') == 'lln':
                    ref_range_value = reference.lln
                elif kwargs.get('range_category') == 'uln':
                    ref_range_value = reference.uln
                else:
                    raise TypeError('Invalid value for keyword argument \'range_category\' for get_reference_range(). You passed \'%s\'' % kwargs.get('range_category'))   
    return ref_range_value 
