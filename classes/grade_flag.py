from django.db.models import Q
from bhp_common.utils import round_up, get_age_in_days
from lab_flag.classes import Flag, BaseDescriptor
from lab_grading.models import GradingListItem




class GradeFlag(Flag):

    """
from datetime import datetime, date
from lab_grading.classes import GradeFlag
flag = GradeFlag()
flag
flag.__dict__
flag.flag
flag.flag = 'pp'
flag.dob=datetime.today()
flag.gender='F'
flag.hiv_status='ANY'
g=GradingListItem.objects.filter(lln__isnull=False)
test_code=g[0].test_code
flag.test_code=test_code
flag.drawn_datetime=datetime.today()
flag.result_item_value = 9
flag.flag
flag.result_item_value = 55
flag.flag
    """

    

    def __init__(self, **kwargs):

        self.REFLIST = 'DAIDS_2004'
        super(GradeFlag, self).__init__(**kwargs)

    def get_flag(self):

        #get age in days using the collection date as a reference
        age_in_days = get_age_in_days(self.drawn_datetime, self.dob)

                
        #filter for the reference items for this list and this testcode, gender
        if self.hiv_status:
            qset = (Q(hiv_status__iexact=self.hiv_status.lower()) | Q(hiv_status__iexact='any'))
        else:
            qset = (Q(hiv_status__iexact='any'))                
        grading_list_items = GradingListItem.objects.filter(
                                qset,
                                grading_list__name__iexact=self.REFLIST,
                                test_code=self.test_code, 
                                gender__icontains=self.gender,
                                )    
        grade = {}        
        if grading_list_items:
            for reference_list_item in grading_list_items:
                #find the record for this age 
                if reference_list_item.age_low_days() <= age_in_days and reference_list_item.age_high_days() >= age_in_days:
                    grade['grade'] = '0'
                    grade['range'] = '-'
                    #see if value is in the of range of a grade
                    if round_up(self.result_item_value, self.test_code.display_decimal_places) >= round_up(reference_list_item.lln, self.test_code.display_decimal_places) and round_up(self.result_item_value, self.test_code.display_decimal_places) <= round_up(reference_list_item.uln, self.test_code.display_decimal_places):
                        grade['grade'] = reference_list_item.grade        
                        grade['range'] = '%s - %s'% (round_up(reference_list_item.lln,self.test_code.display_decimal_places), round_up(reference_list_item.uln,self.test_code.display_decimal_places))                                               
        return grade
