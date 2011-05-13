from datetime import *
from bhp_common.utils import round_up, get_age_in_days
from bhp_lab_grading.models import GradingListItem

def calculate_grade(**kwargs):

    REFLIST = 'DAIDS_2004'
    
    result_value = kwargs.get('result_value')
    oTestCode = kwargs.get('test_code')
    datetime_drawn = kwargs.get('datetime_drawn')
    dob=kwargs.get('dob')
    gender=kwargs.get('gender')
    hiv_status=kwargs.get('hiv_status')            

    #get age in days using the collection date as a reference
    age_in_days = get_age_in_days(datetime_drawn, dob)
    
    #filter for the reference items for this list and this testcode, gender
    oGradingListItem = GradingListItem.objects.filter(
                                    grading_list__name__iexact=REFLIST,
                                    test_code=oTestCode, 
                                    gender__icontains=gender,
                                    hiv_status=hiv_status,
                                    )    
    grade=None

    if oGradingListItem:
        for reference_item in oGradingListItem:
            #find the record for this age 
            if reference_item.age_low_days() <= age_in_days and reference_item.age_high_days() >= age_in_days:
                #see if value is in the of range of a grade
                if round_up(result_value, oTestCode.display_decimal_places) >= round_up(reference_item.lln, oTestCode.display_decimal_places) and round_up(result_value, oTestCode.display_decimal_places) <= round_up(reference_item.uln, oTestCode.display_decimal_places):
                    grade=reference_item.grade

    return grade    
