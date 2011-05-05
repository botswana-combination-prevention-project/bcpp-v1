from datetime import *
from dateutil.relativedelta import *
from django import template
from bhp_common.utils import formatted_age
from bhp_research_protocol.models import ResearchClinic
from bhp_lab_core.utils import calculate_reference_range_comment, get_reference_range
register = template.Library()


@register.filter(name='result_age')
def result_age(born, collection_date):
    reference_date = collection_date.date()
    return formatted_age(born, reference_date)

@register.filter(name='result_clinic_name')
def result_clinic_name(site_identifier, protocol_identifier):
    oResearchClinic = ResearchClinic.objects.filter(site__site_identifier__iexact=site_identifier, protocol__protocol_identifier__iexact=protocol_identifier)
    if oResearchClinic:
        clinic_name = oResearchClinic[0]
    else:
        clinic_name = site_identifier    
    return clinic_name

@register.filter(name='filter_validation_by_status')
def filter_validation_by_status(value, status):
    if status == 'R':
        return 'Rejected'
    elif status == 'P':
        return 'Preliminary'
    else:
        return value  

@register.filter(name='grade_flag')
def grade_flag(value, result_item):
    
    test_code = result_item.test_code 
    dob=result_item.result.order.aliquot.receive.patient.dob 
    gender=result_item.result.order.aliquot.receive.patient.gender
    today = date.today()
    
    rdelta = relativedelta(today, dob)
    
    return 'G' 

@register.filter(name='status_flag')
def status_flag(value):
    if value=='F':
        return ''
    else:
        return value    

@register.filter(name='hide_not_final')        
def hide_not_final(value, validation_status):
    if validation_status=='F':
        return value
    else:    
        return '****'
    
@register.filter(name='reference_range_flag')        
def reference_range_flag(value, oResultItem):
    comment  = calculate_reference_range_comment(value, oResultItem)
    return '%s%s' % (comment['low'], comment['high'])

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


@register.filter(name='quantifier')
def quantifier(value):
    if value == '=':
        return ''
    else:
        return value    
    
