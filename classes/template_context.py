class TemplateContext(dict):
   
    """manage the default template context""" 
    
    def __init__(self):
        
        from defaults import TEMPLATE_CONTEXT

        self.data = {}                                

        if TEMPLATE_CONTEXT is not None: self.update(TEMPLATE_CONTEXT)

    
    """def __getitem__(self, key): return self.data[key]
    
    def __setitem__(self, key, item): self.data[key] = item
    
    def update(self, dict=None ): 
        if dict is not None: self.data.update(dict)
        
    def clear(self): self.data.clear()         

    def copy(self):                            
        if self.__class__ is dict:         
            return dict(self.data)         
        import copy                            
        return copy.copy(self)                 

    def keys(self): return self.data.keys()    

    def items(self): return self.data.items()  

    def values(self): return self.data.values()
    
    #def serialize(self): return self.data.serialize()"""
