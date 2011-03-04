from bhp_common.template_context import TemplateContext

class SearchTemplateContext(TemplateContext):
    
    def __init__(self):
        
        TemplateContext.__init__(self)
        
        from defaults import TEMPLATE_CONTEXT
        
        if not TEMPLATE_CONTEXT is none: self.update(TEMPLATE_CONTEXT)
       
