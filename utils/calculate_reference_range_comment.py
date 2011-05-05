from datetime import *
from bhp_common.utils import round_up, get_age_in_days
from bhp_lab_core.models import TestCodeReference
                    
def calculate_reference_range_comment(value, oResultItem):
    """ 
    calculate the reference range comment for a given test_code, value,
    gender and date of birth. Response comment is LO, HI, or PANIC
    Return a dictionary of comments
    """
    
    result_value = value
    oTestCode = oResultItem.test_code 
    oReceive = oResultItem.result.order.aliquot.receive
    oPatient = oResultItem.result.order.aliquot.receive.patient
    #get age in days using the collection date as a reference
    age_in_days = get_age_in_days(oReceive.datetime_drawn, oPatient.dob)

    #filter for records with this testcode    
    oTestCodeReference = TestCodeReference.objects.filter(test_code=oTestCode, gender__icontains=oPatient.gender)    
    
    comment={}
    comment['low']=''
    comment['high']=''
    comment['panic_low']=''        
    comment['panic_high']=''        

    if oTestCodeReference:
        for reference in oTestCodeReference:
            #find the record for this age 
            if reference.age_low_days() <= age_in_days and reference.age_high_days() >= age_in_days:
                #see if value is out of range
                #low? compare with correct decimal places
                if round_up(result_value, oTestCode.display_decimal_places) < round_up(reference.lln, oTestCode.display_decimal_places):
                    comment['low']='LO'
                #high? compare with correct decimal places
                if round_up(result_value, oTestCode.display_decimal_places) > round_up(reference.uln, oTestCode.display_decimal_places):
                    comment['high']='HI'
               
                #if result_value > reference.uln:
                #    comment['panic']='HI'
                #panic?

    return comment
