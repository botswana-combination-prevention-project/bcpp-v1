import copy
from django.conf import settings
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule
from model_rule import ModelRule


class AlreadyRegistered(Exception):
    pass

class NotRegistered(Exception):
    pass       
 
class BucketController(object):
    
    def __init__(self):
        # contains model buckets {model:modelbucket}
        self._registry = {}
        # iterable container object for dashboard rules
        self.dashboard_rules = []
    
    def register(self, model, model_bucket):  
        if model in self._registry:
            if self._registry[model] == model_bucket:
                raise AlreadyRegistered('The model %s is already registered' % model.__name__)
        self._registry[model] = model_bucket
    
    def update(self, instance):
        """ run model rules for this model instance"""
        for model, model_bucket in self._registry.iteritems():
            if instance.__class__ == model:
                for item in dir(model_bucket):
                    if isinstance(getattr(model_bucket, item), ModelRule):
                        getattr(model_bucket, item).run(instance)

    def autodiscover(self):
        """
        copied from django sites and only very slightly modified - erikvw
        
        Auto-discover INSTALLED_APPS admin.py modules and fail silently when
        not present. This forces an import on them to register any admin bits they
        may want.
        """
    
        for app in settings.INSTALLED_APPS:
            mod = import_module(app)
            # Attempt to import the app's bucket module.
            try:
                before_import_registry = copy.copy(bucket._registry)
                import_module('%s.bucket' % app)
            except:
                # Reset the model registry to the state before the last import as
                # this import will have to reoccur on the next request and this
                # could raise NotRegistered and AlreadyRegistered exceptions
                # (see #8245).
                bucket._registry = before_import_registry
    
                # Decide whether to bubble up this error. If the app just
                # doesn't have an admin module, we can ignore the error
                # attempting to import it, otherwise we want it to bubble up.
                if module_has_submodule(mod, 'bucket'):
                    raise
        
bucket = BucketController()        