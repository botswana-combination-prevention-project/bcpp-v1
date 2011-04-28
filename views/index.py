from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from bhp_common.utils import os_variables
from settings import DATABASES
from bhp_lab_core.models import Result, ResultItem
from bhp_lab_result_report.forms import ResultSearchForm
from laboratory.classes import get_my_limit_queryset
from django.core.paginator import Paginator, InvalidPage, EmptyPage


@login_required
def index(request, **kwargs):

    section_name = kwargs.get('section_name')
    search_name = "result"
    result_identifier = kwargs.get('result_identifier')
    limit = 20
    template = 'result_report.html'
    
    if  result_identifier is not None:
        result = get_object_or_404(Result, result_identifier=result_identifier)
        items = ResultItem.objects.filter(result=result)
        
        #raise TypeError(items)
        return render_to_response(template, {
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

        }, context_instance=RequestContext(request))
        
    else:
              
        if request.method == 'POST':
        
            form = ResultSearchForm(request.POST)
            #raise TypeError(form)
            if form.is_valid():
            
                cd = form.cleaned_data
                search_term=cd['result_search_term']
    
                search_results = render_search(
                    search_term=search_term,
                    )
                """
                return render_to_response(template, {
                    'form': form,
                    'search_term': search_term,                 
                    'section_name': section_name, 
                    'search_results': search_results,
                    'report_name': kwargs.get('report_name'), 
                    'report_title': 'Result Search Results',
                    }, context_instance=RequestContext(request))
               """

        else:
            form = ResultSearchForm()
            results = get_my_limit_queryset({'search_results':""}, "result", limit=5)
            search_results  = results['search_results']
            
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
        #raise TypeError(search_results)
        
        return render_to_response(template, { 
            'form': form,
            'section_name': section_name, 
            'report': 'Recent Results',
            'search_results': search_results,
            'report_name': kwargs.get('report_name'),  
            'top_result_include_file': "result_include.html",       
            }, context_instance=RequestContext(request))
        
def render_search(**kwargs):
    return kwargs['search_term']
