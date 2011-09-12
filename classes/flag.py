from types import *
from datetime import datetime, date
from lab_test_code.models import TestCode

class FlagDescriptor(object):
    def __init__(self):
        self.value = None
    def __get__(self, instance, owner):
        if instance.dirty:
            self.__set__(instance)
        return self.value
    def __set__(self, instance):

        if instance.result_item_value and instance.dob and instance.gender and instance.drawn_datetime and instance.test_code and instance.hiv_status:    
            # set reference_flag dictionary
            value = instance.get_flag()
            if not isinstance(value, DictType):
                raise TypeError, 'flag must be of type Dictionary, Got %s' % type(value)
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

class ResultItemValueDescriptor(BaseDescriptor):
    pass

class TestCodeDescriptor(BaseDescriptor):
    def __set__(self, instance, value):
        if isinstance(value, (TestCode, NoneType)):
            self.value = value
            instance.dirty = True 
        else:
            raise TypeError, '%s expected type TestCode, Got %s' % (self, type(value))

class HivStatusDescriptor(BaseDescriptor):
    def __set__(self, instance, value):
        if isinstance(value, (StringTypes, NoneType)):
            self.value = value
            instance.dirty = True 
        else:
            raise TypeError, '%s expected type string, Got %s' % (self, type(value))


class DobDescriptor(BaseDescriptor):
    def __set__(self, instance, value):
        if isinstance(value, (date, datetime, NoneType)):
            self.value = value
            instance.dirty = True 
        else:
            raise TypeError, '%s expected type date or datetime, Got %s' % (self, type(value))

class GenderDescriptor(BaseDescriptor):
    def __set__(self, instance, value):
        if isinstance(value, (StringTypes, NoneType)):
            self.value = value
            instance.dirty = True 
        else:
            raise TypeError, '%s expected type string, Got %s' % (self, type(value))


class DrawnDatetimeDescriptor(BaseDescriptor):
    def __set__(self, instance, value):
        if isinstance(value, (datetime, NoneType)):
            self.value = value
            instance.dirty = True 
        else:
            raise TypeError, '%s expected type datetime, Got %s' % (self, type(value))



class Flag(object):
    flag = FlagDescriptor()
    hiv_status = HivStatusDescriptor()
    dob = DobDescriptor()
    gender = GenderDescriptor()
    drawn_datetime = DrawnDatetimeDescriptor()
    test_code = TestCodeDescriptor()
    result_item_value = ResultItemValueDescriptor()
    
    def __init__(self, **kwargs):
        self.dirty = True
        self.value = kwargs.get('result_item_value')
        self.test_code = kwargs.get('test_code')
        self.gender = kwargs.get('gender')
        self.drawn_datetime = kwargs.get('drawn_datetime')
        self.dob = kwargs.get('dob')
        self.hiv_status = kwargs.get('hiv_status', 'ANY')                
        
    def get_flag(self):
        pass        
        




