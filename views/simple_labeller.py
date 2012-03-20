from django.shortcuts import render_to_response
from django.template import RequestContext
from bhp_common.utils import os_variables
from lab_barcode.classes import Label
from lab_barcode.forms import LabelForm


def simple_labeller(request, **kwargs):
    
    template = 'label.html'

    if request.method == 'POST':

        form = LabelForm(request.POST)
        
        if form.is_valid():

            specimen_identifier = form.cleaned_data['identifier']
            
            #prnt
            try:
                label = Label(
                            client_ip = '127.0.0.1',
                            specimen_identifier = specimen_identifier,
                            template_name = 'simple_label',
                            )
                label.print_label()  
                                   
            except ValueError, err:
                raise ValueError('Unable to print, is the lab_barcode app configured? %s' % (err,))
            
        form = LabelForm()
   
                                        
    else:

        form = LabelForm()
    
        
    return render_to_response(template, { 
        'form': form,
        'os_variables': os_variables,      
        #'remote_addr' : request.REMOTEADDR,
        }, context_instance=RequestContext(request))