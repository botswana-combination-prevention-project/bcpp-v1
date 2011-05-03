from datetime import *
from dateutil.relativedelta import *
from django import template
from bhp_common.utils import formatted_age
from bhp_research_protocol.models import ResearchClinic
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


@register.filter(name='grade')
def grade(value, result_item):
    
    test_code = result_item.test_code 
    dob=result_item.result.order.aliquot.receive.patient.dob 
    gender=result_item.result.order.aliquot.receive.patient.gender
    today = date.today()
    
    rdelta = relativedelta(today, dob)
    
    return 'G' 

@register.filter(name='hide_not_final')        
def hide_not_final(value, validation_status):
    if validation_status=='F':
        return value
    else:    
        return '****'
    
@register.filter(name='reference_range_comment')        
def reference_range_comment(value, result_item):
    test_code = result_item.test_code 
    comment = 'HILO'
    return comment


@register.filter(name='quantifier')
def quantifier(value):
    if value == '=':
        return ''
    else:
        return value    
    
