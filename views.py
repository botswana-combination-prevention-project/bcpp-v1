from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q
from bhp_common.models import IssueTracker
from bhp_common.utils import os_variables
from mochudi.forms import SearchForm, DateRangeSearchForm


def issue_tracker_search(request):
    """Use the search form to search households"""   
    
    template_filename = u'issuetracker.html'
    help_text = u'' 
     
    if request.method == 'POST':

        form = SearchForm(request.POST)
        
        form.fields['q'].help_text = help_text
        
        if form.is_valid():
            cd = form.cleaned_data
            search_term=cd['q']
         
            qset = (
                Q(item_id__icontains=search_term) |
                Q(item_type__icontains=search_term) |
                Q(rt_number__icontains=search_term) 
                )
        
            object_list = IssueTracker.objects.filter(qset).distinct()
            
            return render_to_response(template_filename, {
                "object_list": object_list,
                "query": search_term,
                "form": form,
                'os_variables': os_variables,                           
            },context_instance=RequestContext(request))
    else:
        form = SearchForm()
        form.fields['q'].help_text = help_text        

    return render_to_response(template_filename, {
        'form': form,
        'os_variables': os_variables,        
        },context_instance=RequestContext(request))
