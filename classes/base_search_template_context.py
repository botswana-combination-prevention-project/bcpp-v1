from bhp_common.classes.base_template_context import BaseTemplateContext

class BaseSearchTemplateContext(BaseTemplateContext):
    
    """subclass of BaseTemplateContext that may add search specific kw/value to the context"""
    
    def __init__(self, **kwargs):
        
        #init base class which loads default context from bhp_common
        BaseTemplateContext.__init__(self)
        
        #load bhp_search default context
        #if not TEMPLATE_CONTEXT is None: self.update(**TEMPLATE_CONTEXT)
        
        self['template'] = "search.html" 
        #self['search_by'] = ""
        self['search_results'] = ""        
        self['dbname']="default"      
        #self['search_helptext'] = ""
        #self['queryset_label'] = ""
        #self['queryset_label_branch'] = ""
        #self['order_by'] = ""
        #self['result_include_file'] = ""
        



