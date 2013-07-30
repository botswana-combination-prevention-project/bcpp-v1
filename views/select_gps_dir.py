import os
# Import django modules
from django.shortcuts import render_to_response
from django.template import RequestContext

def select_gps_dir(request, **kwargs):
    """
    """
    
    dir_list = os.popen('ls /Volumes').read().split('\\')
    template = 'select_gps_dir.html'
    mapper_name = kwargs.get('mapper_name', '')
        
    return render_to_response(
            template, {
                'mapper_name': mapper_name,
                'dir_list': dir_list
            },
            context_instance=RequestContext(request)
        )
