import sys, socket, re
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
from settings import DATABASES
from laboratory.classes import get_my_limit_queryset
from bhp_lab_core.utils import fetch_receive_from_dmis, fetch_lists_from_dmis
from bhp_lab_core.models import Result
from bhp_lab_result_report.forms import ResultSearchForm

def result_index(request, **kwargs):
     
    section_name = kwargs.get('section_name')
    search_name = kwargs.get('search_name')
    template = 'section_%s.html' % (section_name)
    process_status = kwargs.get('process_status')
    search_results = ''
 
    
    #fetch_lists_from_dmis()

    #fetch_receive_from_dmis(process_status)
    """
    if search_name == 'receive':
        form = ResultSearchForm(request.POST)
        return render_to_response(template, { 
            'form': form,
            'section_name': section_name, 
            'report': 'Recent Results',
            'search_results': search_results,
            'report_name': kwargs.get('report_name'),         
        }, context_instance=RequestContext(request))  
    """

    if section_name ==  'result':
        query_label = 'result_%s' % process_status
    else:
        query_label = 'receive_%s' % process_status
    
    raise TypeError(query_label)
    
    result = get_my_limit_queryset({'search_results':""},query_label , limit=5)
        
    search_results  = result['search_results']
    
    paginator = Paginator(search_results, 150)                                    
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        search_results = paginator.page(page)
    except (EmptyPage, InvalidPage):
        search_results = paginator.page(paginator.num_pages)    
    

    
    return render_to_response(template, { 
        'selected': section_name, 
        'section_name': section_name,
        'search_name': search_name,   
        'process_status': process_status,     
        'search_results': search_results,          
        'top_result_include_file': "result_include.html",
        'database': DATABASES,     
       
    }, context_instance=RequestContext(request))
