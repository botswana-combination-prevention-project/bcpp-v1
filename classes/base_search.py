from bhp_common.classes import BaseTemplateContext
from base_search_template_context import BaseSearchTemplateContext

class BaseSearch(BaseSearchTemplateContext):
    
    """ 
        a base class for search forms/result set 
    
        Inherets a base context specific to search
        
        adds 
        
        section_name, 
        search_name, 
        result_include_file 
        
        and
        
        get_labeled_queryset() (which you have to override)
        
    """

    def __init__(self, request, **kwargs):
        
        BaseSearchTemplateContext.__init__(self, **kwargs)

        

        """ 
            search_name:              
            Comes as a parameter from the Url
        """

        if kwargs.get('search_name') is None:
            raise TypeError('BaseSearch requires keyword/value for key \'search_name\'. None given.')
        else:
            self['search_name'] =  kwargs.get('search_name')
        
        """
           result_include_file: if you look at the base_search.html you'll see that 
           the result set block refers to an include file.  
        """
        
        if kwargs.get('result_include_file') is None:
            self['result_include_file'] = '%s%s' % (self['search_name'], "_include.html")
                    
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

