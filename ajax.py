from datetime import date, datetime
from django.db.models import Max
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from lab_clinic_api.models import Lab, Result, ResultItem, UpdateLog
from lab_clinic_api.classes import ResultContext, LabContext
from lab_import_dmis.classes import Dmis

@dajaxice_register
def plot_longitudinal_results(request, subject_identifier, test_code):
    dajax = Dajax()
    rendered = render_to_string('plot_result.html', {'subject_identifier': subject_identifier, 'test_code': test_code })    
    dajax.assign('#left_table','innerHTML',rendered)
    return dajax.json()
    
@dajaxice_register
def updating(request):
    
    dajax = Dajax()

    dajax.assign('#x_results','innerHTML','Contacting lab,<BR>please wait...<BR>')
    
    return dajax.json()

@dajaxice_register
def update_result_status(request, subject_identifier):

    dajax = Dajax()

    if subject_identifier:            
        
        dmis = Dmis()
        dmis.fetch(subject_identifier=subject_identifier, lab_db='lab_api')

        labs = Lab.objects.fetch(subject_identifier=subject_identifier)
        if labs:
            results = Result.objects.fetch(subject_identifier=subject_identifier, labs=labs)
            if results:
                ResultItem.objects.fetch(subject_identifier=subject_identifier, results=results)        
        
        # temp workaround, delete all without a result until
        # i can get this to import correctly
        if Lab.objects.filter(subject_identifier=subject_identifier, result__isnull=True):
            Lab.objects.filter(subject_identifier=subject_identifier, result__isnull=True).delete()        
        labs = Lab.objects.fetch(subject_identifier=subject_identifier)
        aggr = UpdateLog.objects.filter(subject_identifier=subject_identifier).aggregate(Max('update_datetime'))
        if isinstance(aggr['update_datetime__max'], (date,datetime,)):
            lab_last_updated = aggr['update_datetime__max']
        else:    
            lab_last_updated = None
                
        rendered = render_to_string('result_status_bar.html', {'results': labs, 'lab_last_updated': lab_last_updated})

        dajax.assign('#x_results','innerHTML',rendered)
    
    return dajax.json()
    
    
"""
registered_subjects = RegisteredSubject.objects.all()
for registered_subject in registered_subjects:
    subject_identifier = registered_subject.subject_identifier
    labs = Lab.objects.fetch(subject_identifier=subject_identifier)
    if labs:
        results = Result.objects.fetch(subject_identifier=subject_identifier, labs=labs)
        if results:
            x= ResultItem.objects.fetch(subject_identifier=subject_identifier, results=results)
    print subject_identifier            
"""                    
  
  
@dajaxice_register
def view_result_ajax(request, result_identifier):
    
    dajax = Dajax()

    result_context = ResultContext(result_identifier=result_identifier)
    
    rendered = render_to_string('clinic_result_report.html', result_context.context )
    
    dajax.assign('#left_table','innerHTML',rendered)
    
    return dajax.json()


@dajaxice_register
def view_receive_ajax(request, receive_identifier):

    print  receive_identifier   
    dajax = Dajax()

    lab_context = LabContext(receive_identifier=receive_identifier)
    
    rendered = render_to_string('clinic_result_report.html', lab_context.context )
    
    dajax.assign('#left_table','innerHTML',rendered)
    
    return dajax.json()

