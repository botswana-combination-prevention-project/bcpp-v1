from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from mpepu.classes import SearchByWord, SearchByWeek, SearchByDate

@login_required
def search(request, **kwargs):   
    
    search_by=kwargs.get('search_by')
    if search_by=='date':
        search = SearchByDate(request, **kwargs)
    elif search_by=='week':
        search = SearchByWeek(request, **kwargs)
    else:
        search = SearchByWord(request, **kwargs)
    search.prepare(request) 
    search.prepare_form(request, **kwargs)
    if search.ready:
        search.search(request, **kwargs)
        search.paginate(request.GET.get('page', '1'))       
    return render_to_response(
              search.context.get('template'),
              search.context,
              context_instance=RequestContext(request))