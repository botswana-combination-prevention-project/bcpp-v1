from datetime import datetime, date, time
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from bhp_common.utils import os_variables
from bhp_describer.forms import DescriberForm
from bhp_describer.classes import DataDescriber

@login_required
def data_describer(request, **kwargs):

    section_name = kwargs.get('section_name')
    template = 'data_description.html'
    if request.method == 'POST':
        
        form = DescriberForm(request.POST)
      
        if form.is_valid():

            dd = DataDescriber(form.cleaned_data['app_label'], form.cleaned_data['model_name'])
            summary = dd.summarize()
            group = dd.group()    
            #new_group = dd.for_template()
                
            return render_to_response(template, {
                'form': form,
                'table': summary['table'],
                'summary_fields': summary['fields'],
                'group_fields': group['fields'],
                'section_name': section_name, 
                #'os_variables': os_vars, 
                }, context_instance=RequestContext(request))

    else:
        form = DescriberForm()

    return render_to_response(template, { 
        'form': form,
        'table': '',
        'summary_fields':{},
        'group_fields': {},                                
        'section_name': section_name, 
        'report': ''  ,
        #'os_variables': os_vars,  
        'report_name': kwargs.get('report_name'),         
        }, context_instance=RequestContext(request))

