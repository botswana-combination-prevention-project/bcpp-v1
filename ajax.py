from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import get_model
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from lab_requisition.classes import ClinicRequisitionLabel

@dajaxice_register
def print_label(request, app_label, model_name, requisition_identifier):

    dajax = Dajax()
    requisition_model = get_model(app_label, model_name)

    if requisition_model:
        requisition = requisition_model.objects.filter(requisition_identifier=requisition_identifier)
        if requisition:
            for cnt in range(requisition[0].item_count_total, 0, -1):
                label = ClinicRequisitionLabel(
                            client_ip = request.META['REMOTE_ADDR'],
                            item_count = cnt, 
                            requisition = requisition[0],
                            )
                label.print_label() 
                
            #print_message = 'Label for specimen %s has been sent to the printer' % requisition_identifier                   
            print_message = '<ul class="messagelist"><li class="info">%s for specimen %s at %s</li></ul>' % (label.message, requisition_identifier, datetime.today().strftime('%H:%M'))
        else:
            print_message = '<ul class="messagelist"><li class="error">Label did not print, complete the requisition first.</li></ul>'           
    else:            
        print_message = "Label did not print."


    dajax.assign('#print_message','innerHTML',print_message)
    return dajax.json()
  
