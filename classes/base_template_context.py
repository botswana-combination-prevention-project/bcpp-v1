from django.conf import settings
from bhp_common.utils import os_variables


class BaseTemplateContext(dict):
   
    """Descriptor for the default template context""" 
    
    def __init__(self, **kwargs):
        self.data = {}                                
        defaults = {
            'extend': "base_site.html", #required, but this default will avoid an error           
            'template': "", #required
            'report_title': "",
            'section_name': "",
            'os_variables': os_variables,
            'sql':"",
            'database': settings.DATABASES['default'],
            }
        self.update(**defaults)
        #section_name, for example 'clinic', 'lab', 'admin', 'surveys' comes as a parameter from the Url
        if kwargs.get('section_name') is None:
            raise TypeError('BaseSearch requires keyword/value for key \'section_name\'. None given.')
        else:
            self['section_name'] =  kwargs.get('section_name')
    
    def context(self): 
        return self.data
        
    def __getitem__(self, key):
        return self.data[key]
    
    def __setitem__(self, key, item):
        self.data[key] = item
    
    def update(self, **kwargs ): 
        keys = kwargs.keys()
        for kw in keys:
            self.data.update({ kw:kwargs[kw] })
        
    def clear(self): 
        self.data.clear()         

    def copy(self):                            
        if self.__class__ is dict:         
            return dict(self.data)         
        import copy                            
        return copy.copy(self)                 

    def keys(self): 
        return self.data.keys()    

    def items(self): 
        return self.data.items()  

    def values(self): 
        return self.data.values()
    
