from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from lab_clinic_api.forms import ResultSearchForm


@login_required
def index(request, **kwargs):

    section_name = kwargs.get('section_name')
    report_title = 'Result Report'
    template = 'section_specimens.html'

    form = ResultSearchForm

    return render_to_response(template, {
        'form': form,
        'section_name': section_name,
        'report_title': report_title,
        'report_name': kwargs.get('report_name'),
        }, context_instance=RequestContext(request))
