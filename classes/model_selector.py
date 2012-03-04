from django.db.models import get_model, get_models
from django.conf import settings

class AppLabelDescriptor(object):

    def __init__(self):
        self.name = 'app_label'
        self.value = None
        self.error = ''
    def __get__(self, instance, owner):
        return self.value
    def __set__(self, instance, value):
        if value in settings.INSTALLED_APPS:
            self.value = value
        else:
            self.value = None            


class ModelSelector(object):

    app_label = AppLabelDescriptor()
    
    def __init__(self, app_label, model_name):
        
        self.app_label = app_label
        self.model_name = model_name
        self.app_labels = None
        self.model_names = None      

        self.model = None
        self.opts = None
        self.table = None

        self.error_message = None
        self.error_type = None
        
        self.get_model()        

    def get_model(self):
        
        if self.app_label not in settings.INSTALLED_APPS:
            self.got_model = False        
            #self.app_labels = [app_label for app_label in settings.INSTALLED_APPS if app_label[0:6] <> 'django' and app_label <> 'south' and get_models(app_label)]
            self.app_labels = [model._meta.app_label for model in get_models() if model._meta.app_label not in ['contenttypes', 'admin','auth', 'sites', 'sessions', 'south']]
            self.app_labels = set(self.app_labels)
            self.app_labels = list(self.app_labels)
            self.app_labels.sort()
            
            self.error_type = 'app_label'
        else:
            self.model_names = [{'module_name':model._meta.module_name, 'verbose_name':model._meta.verbose_name} for model in get_models() if model._meta.app_label == self.app_label and model._meta.verbose_name[-5:] <> 'audit']
            if self.model_name in [m['module_name'] for m in self.model_names]:
                self.model = get_model(self.app_label, self.model_name)
                self.opts = self.model._meta    
                self.table = '%s__%s' % (self.app_label, self.model_name)
                self.error_message = None
                self.error_type = None
            else:
                #self.error_message = 'Model does not exist in application %s.' % self.app_label    
                self.model_name = None
                self.error_type = 'model_name' 
                         
