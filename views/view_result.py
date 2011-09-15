from settings import DATABASES
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from bhp_common.utils import os_variables
from lab_result.models import Result
from lab_result_item.models import ResultItem
from lab_result_report.forms import ResultSearchForm
from laboratory.classes import get_my_limit_queryset
from lab_result_report.classes import ResultContext

@login_required
def view_result(request, **kwargs):

    section_name = 'result'
    search_name = 'result'

    result_identifier = kwargs.get('result_identifier')
    limit = 20
    template = 'result_report.html'
                  
    if result_identifier is not None:
        result = Result.objects.get(result_identifier__exact=result_identifier)
        result_items = ResultItem.objects.filter(result=result)
        
        result_context = ResultContext(result_identifier)
        
        return render_to_response(template, 
            result_context.context, 
            context_instance=RequestContext(request)
            )  
            
        
def render_search(**kwargs):
    return Result.objects.filter(result_identifier=kwargs['search_term'])
