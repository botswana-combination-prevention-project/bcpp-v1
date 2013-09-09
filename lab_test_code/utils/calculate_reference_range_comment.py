from datetime import *
from bhp_common.utils import round_up, get_age_in_days
from lab_test_code.models import TestCodeReferenceListItem
                    
def calculate_reference_range_comment(value, oResultItem):
    
    """ Calculate the reference range comment for a given test_code, value,
    gender and date of birth. Response comment is LO, HI, or PANIC
    Return a dictionary of comments
    """
    
    REFLIST = 'BHPLAB_NORMAL_RANGES_201005'
    
    result_value = value
    oTestCode = oResultItem.test_code 
    oReceive = oResultItem.result.order.aliquot.receive
    oPatient = oResultItem.result.order.aliquot.receive.patient
    #get age in days using the collection date as a reference
    age_in_days = get_age_in_days(oReceive.datetime_drawn, oPatient.dob)
    
    #filter for the reference items for this list and this testcode, gender
    oTestCodeReferenceListItem = TestCodeReferenceListItem.objects.filter(
                                    test_code_reference_list__name__iexact=REFLIST,
                                    test_code=oTestCode, 
                                    gender__icontains=oPatient.gender,
                                    )    

    
    comment={}
    comment['low']=''
    comment['high']=''
    comment['panic_low']=''        
    comment['panic_high']=''        

    if oTestCodeReferenceListItem:
        for reference_item in oTestCodeReferenceListItem:
            #find the record for this age 
            if reference_item.age_low_days() <= age_in_days and reference_item.age_high_days() >= age_in_days:
                #see if value is out of range
                #low? compare with correct decimal places
                if round_up(result_value, oTestCode.display_decimal_places) < round_up(reference_item.lln, oTestCode.display_decimal_places):
                    comment['low']='LO'
                #high? compare with correct decimal places
                if round_up(result_value, oTestCode.display_decimal_places) > round_up(reference_item.uln, oTestCode.display_decimal_places):
                    comment['high']='HI'
               
                #if result_value > reference.uln:
                #    comment['panic']='HI'
                #panic?

    return comment
