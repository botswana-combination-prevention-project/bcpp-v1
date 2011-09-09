from lab_flag.classes import Flag
from lab_grading.models import GradingListItem


class GradeFlag(Flag):

    def get_flag(self):

        grade = {'grade':0}
        
        self.REFLIST = 'DAIDS_2004'

        hiv_status=kwargs.get('hiv_status')            

        #get age in days using the collection date as a reference
        age_in_days = get_age_in_days(self.drawn_datetime, self.dob)
        
        #filter for the reference items for this list and this testcode, gender
        grading_list_items = GradingListItem.objects.filter(
                                        grading_list__name__iexact=self.REFLIST,
                                        test_code=self.test_code, 
                                        gender__icontains=self.gender,
                                        hiv_status=self.hiv_status,
                                        )    
        
        if grading_list_items:
            for reference_item in grading_list_items:
                #find the record for this age 
                if reference_item.age_low_days() <= age_in_days and reference_item.age_high_days() >= age_in_days:
                    #see if value is in the of range of a grade
                    if round_up(self.result_item_value, self.test_code.display_decimal_places) >= round_up(reference_item.lln, self.test_code.display_decimal_places) and round_up(self.result_item_value, self.test_code.display_decimal_places) <= round_up(reference_item.uln, self.test_code.display_decimal_places):
                        grade['grade'] = reference_item.grade        
                        grade['range'] = '%s - %s'% (reference_list_item.lln, reference_list_item.uln)                                               
        return grade
