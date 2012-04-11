import copy
from django.conf import settings
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule


class AlreadyRegistered(Exception):
    pass

class NotRegistered(Exception):
    pass


class LongitudinalHistory(object):
    
    test_codes = []
    drawn_datetime = None
    value = None
    
    
    
    def __init__(self, *args, **kwargs):
        
        self.panel = kwargs.get('panel')

        for p in self.panel:
            for test_code in p.test_code.all():
                self.test_codes.append(test_code.code) 


class LongitudinalHistoryController(object):
    
    def __init__(self):
        # contains LogitudinalHistory classes
        self._registry = {}
    
    def register(self, longitudinal_history_instance):  
        if longitudinal_history_instance in self._registry:
            if self._registry[longitudinal_history_instance.__name__] == longitudinal_history_instance:
                raise AlreadyRegistered('The class %s is already registered' % longitudinal_history_instance.__name__)
        self._registry[longitudinal_history_instance.__name__] = longitudinal_history_instance
    
    def update(self, instance):
        # update the longitudinal history table if this instance has any relevant values
        for longitudinal_history_instance in self._registry.iteritems():
            
            raise TypeError(longitudinal_history_instance)
            """
            if instance.__class__ == model:
                for item in dir(model_bucket):
                    if isinstance(getattr(model_bucket, item), LongitudinalHistory):
                        getattr(model_bucket, item).run(instance, model_bucket.Meta.app_label)
            """
            
    def autodiscover(self):
        """
        copied from django sites and only very slightly modified - erikvw
        
        Auto-discover INSTALLED_APPS admin.py modules and fail silently when
        not present. This forces an import on them to register any admin bits they
        may want.
        """
    
        for app in settings.INSTALLED_APPS:
            mod = import_module(app)
            # Attempt to import the app's longitudinal_history module.
            try:
                before_import_registry = copy.copy(longitudinal_history._registry)
                import_module('%s.longitudinal_history' % app)
            except:
                # Reset the model registry to the state before the last import as
                # this import will have to reoccur on the next request and this
                # could raise NotRegistered and AlreadyRegistered exceptions
                # (see #8245).
                longitudinal_history._registry = before_import_registry
    
                # Decide whether to bubble up this error. If the app just
                # doesn't have an admin module, we can ignore the error
                # attempting to import it, otherwise we want it to bubble up.
                if module_has_submodule(mod, 'longitudinal_history'):
                    raise
    


class LongitudinalHistoryContainer(object):
    """ Container for LongitudinalHistory """
    def __setitem__(self, name, longitudinal_history):
        
        if not isinstance(longitudinal_history, LongitudinalHistory):
            raise AttributeError('%s expects attribute \'%s\' to be instance of LongitudinalHistory.' % (self, longitudinal_history))
        
        if not self[name]:
            self[name] = longitudinal_history
        #raise TypeError()
        
        return object.__setitem__(self, name, longitudinal_history)
    
    def __delattr__(self, name):
        
        if self.longitudinal_historys[name]:
            del self.longitudinal_historys[name]
        
        return object.__delattr__(self, name)

    def __iter__(self):
        return iter(self.longitudinal_historys)
     
    def __next__(self):
        while self.index < len(self.longitudinal_historys):
            yield self.longitudinal_historys[self.index]
            self.index += 1   
    
    def count(self):
        return len(self.longitudinal_historys)    
    
    
longitudinal_history =  LongitudinalHistoryController()   