from django.shortcuts import render_to_response
from django.template import RequestContext


def db_update_index(request):
    """Update coordinates of a household form
    
    """
    
    template = "db_update.html"
    
    return render_to_response(
                template,{},
            context_instance=RequestContext(request)
        )
