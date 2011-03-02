from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Appointment

def appointments_by_weeknumber(request, options):
    """appointments subject / patient"""    

    if options.get('template'):
        template_filename = options['template']
    else:
        template_filename = u'appointments.html'
        
    template_report_title = options['report_title']
    help_text = u'Enter a week number range.'
    
    if request.method == 'POST':
        msg=""
        form = WeekNumberSearchForm(request.POST)
        
        form.fields['date_start'].help_text = help_text
        
        if form.is_valid():

            cd = form.cleaned_data

            week_start=cd['date_start']
            week_end=cd['date_end']
            year = int(cd['year'])

            #this form returns week numbers so convert to datetime
            wb_start = weekBoundaries(2011, int(week_start))
            wb_end = weekBoundaries(2011, int(week_end))
            
            if week_start == week_end:
                week_range="week %s" % (week_start)
            else:
                week_range="weeks %s to %s" % (week_start, week_end)   
             
            date_start = "%s 00:00" % (wb_start[0])
            date_end = "%s 23:59" % (wb_end[1])            
            
            
            if options['filter_label'] == 'default':
                search_results = Appointment.objects.filter(
                    household_structure_member__subjecthouseholdvisitdetail__visit_datetime__gte=date_start, 
                    household_structure_member__subjecthouseholdvisitdetail__visit_datetime__lte=date_end, 
                    household_structure_member__subjectconsent__isnull=True, 
                    household_structure_member__subjectrefusal__isnull=True
                    ).order_by(options['order_by'])            
                   
            if options['filter_label'] == 'subject household visits':
                search_results = SubjectHouseholdVisitDetail.objects.filter(
                    visit_datetime__gte=date_start, 
                    visit_datetime__lte=date_end,
                    ).order_by(options['order_by'])            



            if options['filter_label'] == 'subject clinic visits':
                search_results = SubjectClinicVisitDetail.objects.filter(
                    visit_datetime__gte=date_start, 
                    visit_datetime__lte=date_end,
                    ).order_by(options['order_by'])            

                
            return render_to_response(template_filename, {
                "report_title": options['report_title'],
                "report_helptext": options['report_helptext'],                
                "search_results": search_results,
                "query": {'date_start':wb_start[0], 'date_end':wb_end[1]},
                "week_range":week_range,
                "form": form,
                "help_text": help_text,
                "msg": msg,
            },context_instance=RequestContext(request))
    else:
        form = WeekNumberSearchForm()
        form.fields['date_start'].help_text = help_text
    return render_to_response(template_filename, {
        'form': form,
        "report_title": options['report_title'],
        "report_helptext": options['report_helptext'],                
        },context_instance=RequestContext(request))

