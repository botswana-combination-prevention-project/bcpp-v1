from django.db import models


class ModelInstanceCounter(object):
    
    def __init__(self, producer, app_and_field = {} ):
        
        self.producer = producer
        self.app_and_field = app_and_field
        self.result = {}
            
    def _set(self):
        
        counts = []

        for app_label, key_field in self.app_and_field.iteritems():
            self. model_list = [{'name': model._meta.module_name, 'model':model} 
                                    for model in models.get_models() 
                                    if (model._meta.app_label in app_label) 
                                    and key_field in 
                                    [field.name for field in model._meta.fields] 
                                    and '_audit_id' not in 
                                    [field.name for field in model._meta.fields]
                                   ]
            
            for dct in self.model_list:
                counts.append([dct['name'], dct['model'].objects.filter(hostname_created=self.producer).count()])
    
            counts.sort()
            
            self.result[app_label] = counts
        
        
    def get(self):
        if not self.result:
            self._set()
        return self.result