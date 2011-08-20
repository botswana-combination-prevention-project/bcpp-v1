from django.conf import settings

class ExcludeKeysDescriptor(object):
    
    def __get__(self, instance, owner):
        return self.value
    def __set__(self, instance, arg):
        if arg and isinstance(arg, list):
            self.value = arg        
        else:
            raise AttributeError, "ExcludeKeysDescriptor expects a list. Got %s" % type(arg)
        

class ContextDescriptor(object):
    
    """Descriptior for a template context"""    
    
    def __init__(self, **kwargs):

        self.context = {}
        #self.exclude_keys = []
        self.initialized = False
        for k,v in kwargs.items():
            self.context['k'] = v
    
    def __get__(self, instance, owner):
        return self.context
    
    def __set__(self, instance, arg):

        if not self.initialized and isinstance(arg, dict): 
            self.context = arg

    def add(self, dct):
        """ add a k,v pair or update an existing k"""
        if arg and isinstance(arg, dict):
            # k,v pairs should be passed only after you have initialized context
            for k,v in arg.items():
                self.context[k] = v
        else:
            raise AttributeError, "Can't set/add dict key, value pair for attribute \'context\'. Got key=%s, value=%s" % (self.name, key, value)

    def.remove(self, key):
        """ remove existing key or raise error """
        if key in self.context.keys():
            del self.context[key]
        else:
            raise AttributeError, "Can't \'remove\' dict key from context. Does not exist. Got key=%s" % key                
        
    def.remove_as_dictionary(self, dct):
        if arg and isinstance(arg, dict):
            del self.context[j]

    def remove_as_list(self, remove_keys):

        """ remove keys given a list of keys """

        for key in self.context.keys():
            if key in remove_keys:
                del self.context[key]    
        
                

class BaseContext(object):

    context = ContextDescriptor()

    def __init__(self):
        
        if 'MAIN_APP_LABEL' in settings.keys():
            main_app_label = settings.MAIN_APP_LABEL
        else:
            main_app_label = ''    
            
        self.context = {
            "app_label": main_app_label,
            "hostname": socket.gethostname(),
            "os_variables":os_variables(),
            }        

    def add_to_context(self, dct):
        
        self.add(dct)    
    
