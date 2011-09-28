from datetime import datetime
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.db.models import get_model
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from lab_requisition.classes import ClinicRequisitionLabel

@dajaxice_register
def print_label(request, app_label, model_name, requisition_identifier, message_label='print_message'):

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
                
            if not label.printer_error:
                print_message = '%s for specimen %s at %s from host %s' % (label.message, requisition_identifier, datetime.today().strftime('%H:%M'), request.META['REMOTE_ADDR'])
                li_class = "info"
            else:
                print_message = '%s' % (label.message)
                li_class = "error"
                
        else:
            print_message = 'Label did not print, complete the requisition first.'           
            li_class = "error"            
    else:            
        print_message = "Label did not print."
        li_class = "error"            


    rendered = render_to_string('print_message.html', { 'print_message': print_message, 'li_class': li_class })


    dajax.assign('#'+message_label,'innerHTML',rendered)
    return dajax.json()
  
