from django.utils.translation import ugettext_lazy as _
from bhp_search.forms import SearchForm
from base_search import BaseSearch

class BaseSearchByWord(BaseSearch):

    def __init__(self, request, **kwargs):
        
        BaseSearch.__init__(self, request, **kwargs )
        
        self['report_title'] = "Search %s by word" % (self['search_name'])
        
        #may wish to handlethis as kwargs
        self['search_helptext'] = _(u'Search by search term. ')
        self['extend']= "base_search_by_word.html"  
        self['search_by_name']='word'  
            
        # check **kwargs for queryset_label, otherwise default
        if not kwargs.get('queryset_label') is None:
            self['queryset_label'] = kwargs.get('queryset_label')
        else:
            self['queryset_label'] = '%s_by_word' % (self['search_name'])

        if request.method == 'POST':            

            self['form'] = SearchForm(request.POST)

            if self['form'].is_valid():

                self['search_term']= self['form'].cleaned_data['search_term']
                self['search_result_title'] = 'Results for search term \'%s\'' % (self['search_term'])                
                
                """call your app's get_labeled_queryset"""
                self.get_labeled_queryset(self['queryset_label'], search_term=self['search_term'])
        else:     

            self['form'] = SearchForm()
    
        return 


