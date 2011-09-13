from datetime import *
from bhp_common.utils import round_up, get_age_in_days
from lab_test_code.models import TestCodeReferenceListItem
                    
def get_reference_flag(**kwargs):
    
    """ Calculate the reference range comment for a given test_code, value,
    gender and date of birth. Response comment is LO, HI, or PANIC
    Return a dictionary of comments
    """
    
    REFLIST = 'BHPLAB_NORMAL_RANGES_201005'
    
    result_item_value = kwargs.get('result_item_value')
    test_code = kwargs.get('test_code')
    gender = kwargs.get('gender')
    drawn_datetime = kwargs('drawn_datetime')
    dob = kwargs.get('dob')
    
    #get age in days using the collection date as a reference
    age_in_days = get_age_in_days(drawn_datetime, dob)
    
    #filter for the reference items for this list and this testcode, gender
    reference_list_items = TestCodeReferenceListItem.objects.filter(
                                    test_code_reference_list__name__iexact=REFLIST,
                                    test_code=test_code, 
                                    gender__icontains=gender,
                                    )    

    
    comment={}
    comment['low']=''
    comment['high']=''
    comment['panic_low']=''        
    comment['panic_high']=''        

    if reference_list_items:
        for reference_list_item in reference_list_items:
            #find the record for this age 
            if reference_list_item.age_low_days() <= age_in_days and reference_list_item.age_high_days() >= age_in_days:
                #see if value is out of range
                #low? compare with correct decimal places
                if round_up(result_item_value, test_code.display_decimal_places) < round_up(reference_list_item.lln, test_code.display_decimal_places):
                    comment['low']='LO'
                #high? compare with correct decimal places
                if round_up(result_item_value, test_code.display_decimal_places) > round_up(reference_list_item.uln, test_code.display_decimal_places):
                    comment['high']='HI'
               
                #if result_value > reference.uln:
                #    comment['panic']='HI'
                #panic?

    return comment
