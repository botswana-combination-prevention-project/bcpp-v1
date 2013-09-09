from bhp_common.utils import get_age_in_days
from lab_test_code.models import TestCodeReferenceListItem

def get_reference_range(**kwargs):
    
    REFLIST = 'BHPLAB_NORMAL_RANGES_201005'
    
    ref_range_value = ''

    #get age in days using the collection date as a reference
    drawn_datetime = kwargs.get('datetime_drawn', 'drawn_datetime')
    age_in_days = get_age_in_days(drawn_datetime, kwargs.get('dob'))

    #filter for the reference items for this list and this testcode, gender
    oTestCodeReferenceListItem = TestCodeReferenceListItem.objects.filter(
                                    test_code_reference_list__name__iexact=REFLIST,
                                    test_code=kwargs.get('test_code'), 
                                    gender__icontains=kwargs.get('gender')
                                    )  
                                    

                                          
    #loop to find record for this age_in_days
    if oTestCodeReferenceListItem:
        #raise TypeError(oTestCodeReferenceListItem)
        for reference_item in oTestCodeReferenceListItem:
            #find the record for this age 
            if reference_item.age_low_days() <= age_in_days and reference_item.age_high_days() >= age_in_days:
                if kwargs.get('range_category') == 'lln':
                    ref_range_value = reference_item.lln
                elif kwargs.get('range_category') == 'uln':
                    ref_range_value = reference_item.uln
                else:
                    raise TypeError('Invalid value for keyword argument \'range_category\' for get_reference_range(). You passed \'%s\'' % kwargs.get('range_category'))   

    return ref_range_value 
