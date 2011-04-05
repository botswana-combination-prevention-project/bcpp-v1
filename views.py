import re
from django.shortcuts import render_to_response
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.template import RequestContext
from django.core.exceptions import ValidationError
from bhp_common.utils import os_variables
from bhp_lab_temptables.models import LabError, LabSimpleResult

@login_required
def result_response(request, **kwargs):

    section_name = kwargs.get('section_name')
    
    os_vars = os_variables()

    template = 'result.html'
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
        'os_variables': os_vars, 
        'report_name': kwargs.get('report_name'), 
        }, context_instance=RequestContext(request))



        

