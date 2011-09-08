from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from models import LocalResult

@dajaxice_register
def updating( request ):
    dajax = Dajax()

    dajax.assign('#results','innerHTML','Contacting lab,<BR>please wait...<BR>')
    
    return dajax.json()

@dajaxice_register
def update_result_status( request, subject_identifier ):

    dajax = Dajax()

    if subject_identifier:            
        
        results = LocalResult.objects.fetch(subject_identifier = subject_identifier)
        
        context = {'results': results,}
        
    rendered = render_to_string('result_status_bar.html', context)

    dajax.assign('#results','innerHTML',rendered)
    
    return dajax.json()
  
