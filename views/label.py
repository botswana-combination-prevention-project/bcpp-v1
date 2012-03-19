from django.shortcuts import render_to_response
from django.template import RequestContext
from lab_barcode.classes import Label
from lab_barcode.forms import LabelForm


def label(request, **kwargs):
    
    template = 'label.html'

    if request.method == 'POST':

        form = LabelForm(request.POST)
        if form.is_valid():

            specimen_identifier = form.cleaned_data['specimen_identifier']
            
            #prnt
            try:
                label = Label(
                            client_ip = 'localhost',
                            specimen_identifier = specimen_identifier,
                            )
                label.print_label()  
                                   
            except ValueError, err:
                raise ValueError('Unable to print, is the lab_barcode app configured? %s' % (err,))
            
            
                                        
    else:

        form = LabelForm()
    
        
    return render_to_response(template, { 
        'form': form,
        'label': label,      
        }, context_instance=RequestContext(request))