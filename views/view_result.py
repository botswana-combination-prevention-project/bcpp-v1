from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from lab_clinic_api.classes import ResultContext


@login_required
def view_result(request, **kwargs):

    section_name = 'result'
    search_name = 'result'

    result_identifier = kwargs.get('result_identifier')
    #limit = 20
    template = 'result_report_single.html'
    result_context = ResultContext()
                  
    if result_identifier is not None:
        
        result_context = ResultContext(result_identifier=result_identifier, search_name=search_name, section_name=section_name)
        
    return render_to_response(template, 
        result_context.context, 
        context_instance=RequestContext(request)
        )  

