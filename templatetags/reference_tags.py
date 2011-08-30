from datetime import *
from dateutil.relativedelta import *
from django import template
from lab_test_code.utils import calculate_reference_range_comment, get_reference_range

register = template.Library()

@register.filter(name='lln')        
def lln(test_code, oResultItem):
    oPatient = oResultItem.result.order.aliquot.receive.patient
    datetime_drawn = oResultItem.result.order.aliquot.receive.datetime_drawn
    lln  = get_reference_range(range_category='lln', test_code=test_code, dob=oPatient.dob, gender=oPatient.gender, datetime_drawn=datetime_drawn)
    return lln

@register.filter(name='uln')        
def uln(test_code, oResultItem):
    oPatient = oResultItem.result.order.aliquot.receive.patient
    datetime_drawn = oResultItem.result.order.aliquot.receive.datetime_drawn    
    uln  = get_reference_range(range_category='uln', test_code=test_code, dob=oPatient.dob, gender=oPatient.gender,datetime_drawn=datetime_drawn)
    return uln

@register.filter(name='reference_range_flag')        
def reference_range_flag(value, oResultItem):
    comment  = calculate_reference_range_comment(value, oResultItem)
    return '%s%s' % (comment['low'], comment['high'])

