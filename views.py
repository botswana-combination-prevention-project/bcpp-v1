
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from bhp_common.utils import os_variables
from settings import DATABASES
from utils import all_uphosts

@login_required
def uphosts(request, **kwargs):
    
    template = 'uphosts.html'

    hosts = all_uphosts(**kwargs)



    return render_to_response(template, { 
        'report_title': 'HBC netbooks in the area', 
        'section_name': kwargs.get('section_name'), 
        'os_variables': os_variables,  
        'database': DATABASES,     
        'uphosts':all_uphosts(**kwargs),
        'app_name': kwargs.get('app_name'),
    }, context_instance=RequestContext(request))
