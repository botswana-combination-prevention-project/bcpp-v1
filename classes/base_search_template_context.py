from bhp_common.classes.base_template_context import BaseTemplateContext


class BaseSearchTemplateContext(BaseTemplateContext):
    
    """subclass of BaseTemplateContext that may add search specific kw/value to the context"""
    
    def __init__(self, **kwargs):
        
        BaseTemplateContext.__init__(self, **kwargs)
        
        defaults = {'template':"search.html",
                    'base_search_extender':"section_search.html",
                    'search_results':"",
                    'dbname':"default",
                    'page':None,
                    'magic_url':'',}
        self.update(**defaults)        
        



