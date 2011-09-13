from datetime import date, datetime
from django.db.models import Max
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from lab_clinic_api.models import Lab, Result, ResultItem, UpdateLog

@dajaxice_register
def updating(request):
    
    dajax = Dajax()

    dajax.assign('#x_results','innerHTML','Contacting lab,<BR>please wait...<BR>')
    
    return dajax.json()

@dajaxice_register
def update_result_status(request, subject_identifier):

    dajax = Dajax()

    if subject_identifier:            
        labs = Lab.objects.fetch(subject_identifier=subject_identifier)
        if labs:
            results = Result.objects.fetch(subject_identifier=subject_identifier, labs=labs)
            if results:
                ResultItem.objects.fetch(subject_identifier=subject_identifier, results=results)        
                
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
  
