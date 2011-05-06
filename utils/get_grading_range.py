from bhp_common.utils import round_up, get_age_in_days
from bhp_lab_grading.models import GradingListItem
from bhp_lab_grading.utils import calculate_grade

def get_grading_range(**kwargs):

    REFLIST = 'DAIDS_2004'
    
    ln = None
    
    result_value = kwargs.get('result_value')
    if not result_value:
        raise TypeError('get_grading_range() requires parameter result_value, none given.')                
    oTestCode = kwargs.get('test_code')
    if not oTestCode:
        raise TypeError('get_grading_range() requires parameter test_code, none given.')                
    
    datetime_drawn = kwargs.get('datetime_drawn')
    if not datetime_drawn:
        raise TypeError('get_grading_range() requires parameter datetime_drawn, none given.')                
    
    dob = kwargs.get('dob')
    if not dob:
        raise TypeError('get_grading_range() requires parameter dob, none given.')                

    gender = kwargs.get('gender')
    if not gender:
        raise TypeError('get_grading_range() requires parameter gender, none given.')                
    
    #get age in days using the collection date as a reference
    age_in_days = get_age_in_days(kwargs.get('datetime_drawn'), kwargs.get('dob'))

    grade = calculate_grade(result_value=result_value, 
                                dob=dob, 
                                gender=gender, 
                                datetime_drawn=datetime_drawn, 
                                test_code=oTestCode,
                                )

    #filter for the reference items for this list and this testcode, gender
    oGradingListItem = GradingListItem.objects.filter(
                                    grading_list__name__iexact=REFLIST,
                                    test_code=kwargs.get('test_code'), 
                                    gender__icontains=kwargs.get('gender'),
                                    grade=grade,
                                    )  
                                    
    #loop to find record for this age_in_days
    if oGradingListItem:

        for reference_item in oGradingListItem:
            #find the record for this age 
            if reference_item.age_low_days() <= age_in_days and reference_item.age_high_days() >= age_in_days:
                ln={}
                ln['grade'] = grade
                ln['lower'] = round_up(reference_item.lln,oTestCode.display_decimal_places)
                ln['upper'] = round_up(reference_item.uln, oTestCode.display_decimal_places)

    return ln 
