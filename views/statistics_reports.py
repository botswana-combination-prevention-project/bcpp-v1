from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.safestring import mark_safe
from bhp_calendar.classes import DataCalendar


def statistics_reports(request, **kwargs):
  
    """prepare a month report for display based on queryset_label, month amd year criteria """
  
    if kwargs.get('year'):
        year = int(kwargs.get('year'))  
    else:
        year=''         
    if kwargs.get('month') :
        month = int(kwargs.get('month'))
    else:
        month=''    
    if kwargs.get('report_number'):
        report_number = kwargs('report_number')
    else:
        raise TypeError('statistics_reports requires a value for keyword argument \'report_number\'. None given.')         

    section_name = kwargs.get('section_name')  

    rep = {}
    
    #raise TypeError(queryset_label)
    
    if rep.get('search_results', None):
        rep['report'] = rep['search_results']
    else:
        rep['report'] = ''

    return render_to_response('section_statistics.html',
        rep.context(), 
        context_instance=RequestContext(request))
