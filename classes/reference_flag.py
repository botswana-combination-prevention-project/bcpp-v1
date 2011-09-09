from bhp_common.utils import round_up, get_age_in_days
from lab_test_code.models import TestCodeReferenceListItem
from lab_flag.classes import Flag

class ReferenceFlag(Flag):        

    """
from datetime import datetime, date
from lab_flag.classes import ReferenceFlag
flag = ReferenceFlag()
flag
flag.__dict__
flag.flag
flag.flag = 'pp'
flag.dob=datetime.today()
flag.gender='F'
test_code = TestCode.objects.get(code='HGB')
flag.test_code=test_code
flag.drawn_datetime=datetime.today()
flag.result_item_value = 9
flag.flag
flag.result_item_value = 90
flag.flag
    """

    def get_flag(self):
        """ Calculate the reference range comment for a given test_code, value,
        gender and date of birth. Response comment is LO, HI, or PANIC
        Return a dictionary of comments
        """
        #get age in days using the collection date as a reference
        age_in_days = get_age_in_days(self.drawn_datetime, self.dob)
        #filter for the reference items for this list and this testcode, gender
        reference_list_items = TestCodeReferenceListItem.objects.filter(
                                        test_code_reference_list__name__iexact=self.REFLIST,
                                        test_code=self.test_code, 
                                        gender__icontains=self.gender,
                                        )    
        reference_flag={}
        reference_flag['low']=''
        reference_flag['high']=''
        reference_flag['range']=''
        reference_flag['panic_low']=''        
        reference_flag['panic_high']=''        
        if reference_list_items:
            for reference_list_item in reference_list_items:
                #find the record for this age 
                if reference_list_item.age_low_days() <= age_in_days and reference_list_item.age_high_days() >= age_in_days:
                    #see if value is out of range
                    #low? compare with correct decimal places
                    if round_up(self.result_item_value, self.test_code.display_decimal_places) < round_up(reference_list_item.lln, self.test_code.display_decimal_places):
                        reference_flag['low']='LO'
                        reference_flag['range'] = '%s - %s'% (reference_list_item.lln, reference_list_item.uln)                       
                    #high? compare with correct decimal places
                    if round_up(self.result_item_value, self.test_code.display_decimal_places) > round_up(reference_list_item.uln, self.test_code.display_decimal_places):
                        reference_flag['high']='HI'
                        reference_flag['range'] = '%s - %s'% (reference_list_item.lln, reference_list_item.uln)                       
        return reference_flag
        
