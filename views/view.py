from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from bhp_common.utils import os_variables
from settings import DATABASES
from bhp_lab_core.models import Result, ResultItem


@login_required
def view(request, **kwargs):

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
    
