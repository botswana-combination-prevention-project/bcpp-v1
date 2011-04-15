from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from bhp_common.utils import os_variables
from settings import DATABASES
#from bhp_lab_temptables.models import LabError, LabSimpleResult
from bhp_lab_result_report.forms import ResultSearchForm

@login_required
def index(request, **kwargs):

    section_name = kwargs.get('section_name')

    template = 'result_report.html'
    
    if request.method == 'POST':
        
        form = ResultSearchForm(request.POST)
      
        if form.is_valid():

            cd = form.cleaned_data
            search_term=cd['result_search_term']
    
            search_result = render_search(
                search_term=search_term,
                )
    
            return render_to_response(template, {
                'form': form,
                'search_term': search_term,                 
                'section_name': section_name, 
                'search_result': search_result  ,
                'report_name': kwargs.get('report_name'), 
                'report_title': 'title',
                }, context_instance=RequestContext(request))

    else:
        form = ResultSearchForm()

    return render_to_response(template, { 
        'form': form,
        'section_name': section_name, 
        'report': ''  ,
        'report_name': kwargs.get('report_name'),         
        }, context_instance=RequestContext(request))
        
def render_search(**kwargs):
    return None
