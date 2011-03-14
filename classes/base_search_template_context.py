from bhp_common.classes.base_template_context import BaseTemplateContext

class BaseSearchTemplateContext(BaseTemplateContext):
    
    """subclass of BaseTemplateContext that may add search specific kw/value to the context"""
    
    def __init__(self, **kwargs):
        
        BaseTemplateContext.__init__(self, **kwargs)
        
        self['template'] = "search.html"
        self['base_search_extender'] = "section_search.html" #this template defined in your app
        self['search_results'] = ""        
        self['dbname'] = "default"
        self['page'] = None      
        self['magic_url'] = ''        
        



