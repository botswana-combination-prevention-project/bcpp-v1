from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from lab_clinic_api.classes import ResultContext


@login_required
def view_result(request, **kwargs):

    result_identifier = kwargs.get('result_identifier')
    #if result_identifier is not None:
    result_context = ResultContext(result_identifier)
    #rendered = render_to_string('clinic_result_report.html', result_context.context)
    return render_to_response('clinic_result_report.html',
        result_context.context,
        context_instance=RequestContext(request)
        )
