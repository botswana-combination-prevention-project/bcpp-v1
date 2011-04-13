from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from bhp_variables.models import StudySpecific
from bhp_common.utils import os_variables
from settings import DATABASES
from bhp_lab_temptables.models import LabError, LabSimpleResult

@login_required
def index(request, **kwargs):
    
    warnings = {}
    
    study_specific = StudySpecific.objects.all()
    
    section_name = kwargs.get('section_name')
        
    os_vars = os_variables()

    template = 'result_report.html'

    results = []
   
    result_items = LabError.objects.filter(sample_id__exact='UJ62429') 
    
    if result_items:
        for result_item in result_items:
            row = {}
            row['utestid'] = result_item.utestid
            #row.append(result_item.description)
            row['result'] = result_item.result
            row['result_quantifier'] = result_item.result_quantifier
            #row.append(result_item.assay_date)
            #row.append(result_item.units)
            results.append(row)


    return render_to_response(template, { 
        'results': results,
        'section_name': section_name,        
        'comment':"",
        'warnings': warnings, 
        'bhp_variables': study_specific,
        'os_variables': os_vars,
        'database': DATABASES,     
    },context_instance=RequestContext(request))
