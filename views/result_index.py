import sys, socket, re
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
from settings import DATABASES
from laboratory.classes import get_my_limit_queryset
from bhp_lab_core.utils import fetch_receive_from_dmis

def result_index(request, **kwargs):
    
    section_name = kwargs.get('section_name')
    search_name = 'pending'    
    template = 'section_%s.html' % (section_name)
    process_status = kwargs.get('process_status')
    search_results = ''

    #fetch_receive_from_dmis(process_status)
    
    query_label = 'receive_%s' % process_status

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
        'search_results': search_results,          
        'top_result_include_file': "receive_include.html",
        'database': DATABASES,     
       
    }, context_instance=RequestContext(request))
