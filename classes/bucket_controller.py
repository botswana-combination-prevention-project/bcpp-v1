import copy
from django.conf import settings
from django.db.models import get_model, Q
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
        self._registry = {'scheduled':{}, 'additional':{}}
        # iterable container object for dashboard rules
        self.dashboard_rules = []
        
    def register(self, model, model_bucket, register='scheduled'):  
        """ """
        if register == 'scheduled':
            if model in self._registry['scheduled']:
                if self._registry['scheduled'][model] == model_bucket:
                    raise AlreadyRegistered('The model %s is already registered' % model.__name__)
            self._registry['scheduled'][model] = model_bucket
        elif register == 'additional':
            if model in self._registry['additional']:
                if self._registry['additional'][model] == model_bucket:
                    raise AlreadyRegistered('The model %s is already registered' % model.__name__)
            self._registry['additional'][model] = model_bucket    
        else:
            raise ValueError('Invalid Key for _registry. Got %s' % (register,))    
           
    def update(self, instance):
            
        """ run model rules for this model instance"""
        self.target_model = {'add':[], 'delete':[]}
        AdditionalEntryBucket = get_model('bhp_entry', 'additionalentrybucket')

        if self._registry['scheduled']:
            """ update status for scheduled entries """
            for model, model_bucket in self._registry['scheduled'].iteritems():
                if instance.__class__ == model:
                    for item in dir(model_bucket):
                        if isinstance(getattr(model_bucket, item), ModelRule):
                            getattr(model_bucket, item).run(instance, model_bucket.Meta.app_label)
        

        if self._registry['additional']:
            """ add / delete additional entries """ 
            for model, model_bucket in self._registry['additional'].iteritems():
                if instance.__class__ == model:
                    for item in dir(model_bucket):
                        if isinstance(getattr(model_bucket, item), ModelRule):
                            tpl = getattr(model_bucket, item).run(instance, model_bucket.Meta.app_label)            
                            for item in tpl[0]:
                                self.target_model['add'].append(item)
                            for item in tpl[1]:
                                self.target_model['delete'].append(item)
            
            #delete if target model not in self.target_model_add
            #self.target_model['delete'] = [model for model in self.target_model['delete'] if model['model'] not in [model['model'] for model in self.target_model['add']]]    
            
            #delete additional entry bucket instances 
            for model in self.target_model['delete']:
                if AdditionalEntryBucket.objects.filter(registered_subject = model['registered_subject'],
                                                        content_type_map__app_label = model['model']._meta.app_label,
                                                        content_type_map__model = model['model']._meta.object_name.lower()):
                    
                    additional_entry = AdditionalEntryBucket.objects.get(registered_subject = model['registered_subject'],
                                                        content_type_map__app_label = model['model']._meta.app_label,
                                                        content_type_map__model = model['model']._meta.object_name.lower())
                    #delete if not keyed
                    if not additional_entry.is_keyed():
                        additional_entry.delete()
            
            #add additional entry bucket instances 
            for model in self.target_model['add']:
                AdditionalEntryBucket.objects.add_for(
                    registered_subject = model['registered_subject'],
                    model = model['model'],
                    qset = Q(registered_subject=model['registered_subject']),
                    )             
             
    
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
        