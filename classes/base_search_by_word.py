from bhp_search.forms import SearchForm
from base_search import BaseSearch

class BaseSearchByWord(BaseSearch):

    def __init__(self, request, **kwargs):
        
        BaseSearch.__init__(self, request, **kwargs )
        
        defaults={'report_title':'Search {0} by word'.format(self.get('search_name')),
                  'search_helptext':'Search by search term.',
                  'extend':'base_search_by_word.html',  
                  'search_by_name':'word',} 
        self.update(**defaults) 
        
        options={}
        # check **kwargs for queryset_label, otherwise default
        if kwargs.get('queryset_label'):
            options.update({'queryset_label':kwargs.get('queryset_label')})
        else:
            options.update({'queryset_label':'%s_by_word'.format(self.get('search_name'))})
        if ((request.method == 'GET' and not request.GET == {}) or ( request.method == 'POST' and not request.POST == {})):            
            if request.method == 'POST':
                options.update({'form':SearchForm(request.POST)})
            elif request.method == 'GET':    
                options.update({'form':SearchForm(request.GET)})
            else:
                raise TypeError('Request method unknown. Expected POST or GET. See BaseSearchByWeek')
            if self.get('form').is_valid():
                if request.method == 'POST':
                    options.update({'magic_url':request.POST.urlencode()})                
                elif request.method == 'GET':    
                    options.update({'magic_url':request.GET.urlencode()})                
                options.update({'search_term':self.get('form').cleaned_data.get('search_term')})
                options.update({'search_result_title':'Results for search term \'{0}\''.format(self.get('search_term'))})              
                """call your app's get_labeled_queryset"""
                self.get_labeled_queryset(self.get('queryset_label'), search_term=self.get('search_term'))
        else:     
            options.update({'form':SearchForm()})
        self.update(**options)    
        return 


