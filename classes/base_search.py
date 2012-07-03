#from bhp_common.classes import BaseTemplateContext
from base_search_template_context import BaseSearchTemplateContext


class BaseSearch(BaseSearchTemplateContext):
    
    def __init__(self, request, **kwargs):
        BaseSearchTemplateContext.__init__(self, **kwargs)
        defaults={}
        #search_name: comes as a parameter from the Url
        if not kwargs.get('search_name', None):
            raise TypeError('BaseSearch requires keyword/value for key \'search_name\'. None given.')
        else:
            defaults.update({'search_name':kwargs.get('search_name')})
        # result_include_file: if you look at the base_search.html you'll see that 
        # the result set block refers to an include file.  
        if not kwargs.get('result_include_file', None):
            defaults.update({'result_include_file':'{0}{1}'.format(self.get('search_name'), "_include.html")})
        self.update(defaults)
                    
    def get_labeled_queryset(self, queryset_label, **kwargs):
        
        """ 
            get a queryset based on a pass lable value
            this must be overridden by the main app as it will make references to local models 
            
            for example, in your app 
            
            class SearchByWeek(BaseSearchByWeek):
                def get_labeled_queryset(self, queryset_label, **kwargs):
                    get_my_labeled_queryset(self, queryset_label, **kwargs)
                    
            ...and then define get_my_labeled_queryset as well  

        """
        raise TypeError("BaseSearch.get_labeled_queryset must be overridden by child class")        
        
    def form(self, post=None):
        """you can override this method to use a different form"""
        pass

