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
    oResearchClinic = Protocol.objects.filter(site__site_identifier__iexact=site_identifier, protocol__protocol_identifier__iexact=protocol_identifier)
    
    
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
    
@register.filter(name='quantifier')
def quantifier(value):
    if value == '=':
        return ''
    else:
        return value    
    
