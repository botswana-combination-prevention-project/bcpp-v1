import re
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.exceptions import ValidationError
from bcpp.classes import SearchByWeek, SearchByDate, SearchByWord

@login_required
def search_response(request, **kwargs):
    """
    """   
    
    # initiate a default search context
    search_by =  kwargs.get('search_by')
    
    if search_by == 'week':    
        SearchResponse = SearchByWeek(request,**kwargs)

    elif search_by == 'date':    
        SearchResponse = SearchByDate(request,**kwargs)
        SearchResponse.get_response(request,**kwargs)

    elif search_by == 'word':    
        SearchResponse = SearchByWord(request,**kwargs)
        
    else:
        raise ValidationError(u'Unknown keyword value \'%s\' for [\'search_by\'] in bcpp search_response.' % (search_by) )      

    # remove page= from GET url
    SearchResponse['magic_url'] = re.sub('\&page=\d+|\?page=\d+\&' , '' , SearchResponse['magic_url'])

    paginator = Paginator(SearchResponse['search_results'], 25)                                    
        # Make sure page request is an int. If not, deliver first page.
    try:
        SearchResponse['page'] = int(request.GET.get('page', '1'))
    except ValueError:
        SearchResponse['page'] = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        SearchResponse['search_results'] = paginator.page(SearchResponse['page'])
    except (EmptyPage, InvalidPage):
        SearchResponse['search_results'] = paginator.page(paginator.num_pages)

    #raise TypeError(SearchResponse['search_results'].object_list)               
    return render_to_response(SearchResponse['template'],
            SearchResponse.context(),
            context_instance=RequestContext(request))
    
    

        

