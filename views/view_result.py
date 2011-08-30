from settings import DATABASES
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from bhp_common.utils import os_variables
from lab_result.models import Result
from lab_result_item.models import ResultItem
from bhp_lab_result_report.forms import ResultSearchForm
from laboratory.classes import get_my_limit_queryset


@login_required
def view_result(request, **kwargs):

    section_name = 'result'
    search_name = 'result'

    result_identifier = kwargs.get('result_identifier')
    limit = 20
    template = 'result_report.html'
                  
    if result_identifier is not None:
        oResult = Result.objects.get(result_identifier__exact=result_identifier)
        oResultItems = ResultItem.objects.filter(result=oResult)
        
        context = {
        'result': oResult,
        'receive': oResult.order.aliquot.receive,
        'order': oResult.order,
        'aliquot': oResult.order.aliquot,
        'result_items': oResultItems,
        'action':"view",        
        'section_name': section_name,
        'search_name': search_name,        
        'result_include_file': "detail.html",
        'receiving_include_file':"receiving.html",
        'orders_include_file': "orders.html",
        'result_items_include_file': "result_items.html",
        'top_result_include_file': "result_include.html",
        }
        
        return render_to_response(template, 
            context, 
            context_instance=RequestContext(request)
            )  
            
@login_required
def xxxview_result(request, **kwargs):

    section_name = kwargs.get('section_name')
    search_name = "result"
    result_identifier = kwargs.get('result_identifier')
    limit = 20
    template = 'result_report.html'
                  
    if result_identifier is not None:
        result = get_object_or_404(Result, result_identifier=result_identifier)
        items = ResultItem.objects.filter(result=result)
        
        payload = {
        'result': result,
        'receive': result.order.aliquot.receive,
        'order': result.order,
        'aliquot': result.order.aliquot,
        'result_items': items,
        'section_name': section_name,
        'result_include_file': "detail.html",
        'receiving_include_file':"receiving.html",
        'orders_include_file': "orders.html",
        'result_items_include_file': "result_items.html",
        'top_result_include_file': "result_include.html",
        }
        
        return render_to_response(template, payload, context_instance=RequestContext(request))   
    
            
    #raise TypeError(form)    
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
        'section_name': section_name, 
        'report': 'Recent Results',
        'search_results': search_results,
        'report_name': kwargs.get('report_name'),  
        'top_result_include_file': "result_include.html",       
        }, context_instance=RequestContext(request))
        
def render_search(**kwargs):
    return Result.objects.filter(result_identifier=kwargs['search_term'])
