from datetime import datetime, date
from bhp_common.utils import round_up, get_age_in_days
from lab_test_code.models import TestCodeReferenceListItem

"""
flag = Flag()
flag
<Flag object at 0x9fc3e8c>
flag.__dict__
{'result_item_value': None, 'REFLIST': 'BHPLAB_NORMAL_RANGES_201005', 'dirty': True}
flag.flag
{}
flag.flag = 'pp'
Traceback (most recent call last):
  File "<console>", line 1, in <module>
TypeError: __set__() takes exactly 2 arguments (3 given)
flag.dob=datetime.today()
flag.gender='F'
flag.test_code='HGB'
flag.drawn_datetime=datetime.today()
flag.flag
"""

class FlagDescriptor(object):
    def __init__(self):
        self.value = None
    def __get__(self, instance, owner):
        if instance.dirty:
            self.__set__(instance)
        return self.value
    def __set__(self, instance):
        if instance.dob and instance.gender and instance.drawn_datetime and instance.test_code:    
            # set reference_flag dictionary
            value = instance.get_reference_flag()
            if not isinstance(value, dict):
                raise TypeError, 'reference_flag must be of type Dictionary, Got %s' % type(value)
            instance.dirty = False                
            self.value = value
        else:
            self.value = {}



class BaseDescriptor(object):
    def __init__(self):
        self.value = None
    def __get__(self, instance, owner):
        return self.value
    def __set__(self, instance, value):
        self.value = value
        instance.dirty = True 



class TestCodeDescriptor(BaseDescriptor):
    pass



class DobDescriptor(BaseDescriptor):
    pass



class GenderDescriptor(BaseDescriptor):
    pass



class DrawnDatetimeDescriptor(BaseDescriptor):
    pass



class Flag(object):
    flag = FlagDescriptor()
    dob = DobDescriptor()
    gender = GenderDescriptor()
    drawn_datetime = DrawnDatetimeDescriptor()
    test_code = TestCodeDescriptor()
    def __init__(self, **kwargs):
        self.dirty = True
        self.result_item_value = kwargs.get('result_item_value')
        self.test_code = kwargs.get('test_code')
        self.gender = kwargs.get('gender')
        self.drawn_datetime = kwargs.get('drawn_datetime')
        self.dob = kwargs.get('dob')
        self.REFLIST = 'BHPLAB_NORMAL_RANGES_201005'
    def get_reference_flag(self, **kwargs):
        """ Calculate the reference range comment for a given test_code, value,
        gender and date of birth. Response comment is LO, HI, or PANIC
        Return a dictionary of comments
        """
        #get age in days using the collection date as a reference
        age_in_days = get_age_in_days(drawn_datetime, dob)
        #filter for the reference items for this list and this testcode, gender
        reference_list_items = TestCodeReferenceListItem.objects.filter(
                                        test_code_reference_list__name__iexact=self.REFLIST,
                                        test_code=self.test_code, 
                                        gender__icontains=gender,
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
                    if round_up(result_item_value, self.test_code.display_decimal_places) < round_up(reference_list_item.lln, self.test_code.display_decimal_places):
                        reference_flag['low']='LO'
                        reference_flag['range'] = '$(lln) - $(uln)'.format(lln=reference_list_item.lln, uln=reference_list_item.uln)                        
                    #high? compare with correct decimal places
                    if round_up(result_item_value, self.test_code.display_decimal_places) > round_up(reference_list_item.uln, self.test_code.display_decimal_places):
                        reference_flag['high']='HI'
                        reference_flag['range'] = '$(lln) - $(uln)'.format(lln=reference_list_item.lln, uln=reference_list_item.uln)                       
        return reference_flag
        
