from datetime import datetime
from django.db import models
from django.db.models import get_model, get_models
from django.db.models import DateTimeField, DateField, IntegerField, DecimalField, CharField
from django.db.models import Count, Avg, Max, Min, StdDev, Variance
from django.conf import settings
from bhp_describer.models import Related

"""
from bhp_describer.classes import DataDescriber
d = DataDescriber('mochudi_subject', 'qn002sectionone')
d.summarize()
d.group()
d.group_m2m()
d.export_as_csv()
"""

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


class DataDescriber(object):

    app_label = AppLabelDescriptor()
    
    def __init__(self, app_label, model_name):
        
        self.app_label = app_label
        self.model_name = model_name
        self.app_labels = None
        self.model_names = None      

        self.model = None
        self.opts = None
        self.table = None

        self.summary = {} 
        self.grouping = {}           
        self.grouping_m2m = {}     

        self.error_message = None
        self.error_type = None

        self.get_model()
        
    def get_model(self):
        
        if self.app_label not in settings.INSTALLED_APPS:
            self.got_model = False        
            self.app_labels = [app_label for app_label in settings.INSTALLED_APPS if app_label[0:6] <> 'django' and app_label <> 'south']
            #self.error_message = 'App_label %s does not exist in this project.' % self.app_label
            self.error_type = 'app_label'
        else:
            self.model_names = [model._meta.module_name for model in get_models() if model._meta.app_label == self.app_label]
            if self.model_name in self.model_names:
                self.model = get_model(self.app_label, self.model_name)
                self.opts = self.model._meta    
                self.table = '%s__%s' % (self.app_label, self.model_name)
                self.error_message = None
                self.error_type = None
            else:
                #self.error_message = 'Model does not exist in application %s.' % self.app_label    
                self.model_name = None
                self.error_type = 'model_name'                

    def summarize(self):        

        # basic summary
        summarize = {}        
        if self.model:
            q={}
            self.summary = {}
            for field in self.opts.fields:
                if isinstance(field, (DateTimeField, DateField)):
                    aggregates = self.model.objects.all().aggregate(Count(field.name), Max(field.name), Min(field.name))
                    new_aggregates = {}                
                    for key, value in aggregates.items():
                        k = key.split('__')
                        new_aggregates[k[1]] = value
                    q = new_aggregates     
                        
                elif isinstance(field, (IntegerField, DecimalField)):
                    aggregates = self.model.objects.all().aggregate(Count(field.name), Avg(field.name), Max(field.name), Min(field.name), StdDev(field.name), Variance(field.name))    
                    new_aggregates = {}                
                    for key, value in aggregates.items():
                        k = key.split('__')
                        new_aggregates[k[1]] = value
                    q = new_aggregates     


                #elif isinstance(field, (CharField)):
                #    q = self.model.objects.all().aggregate(Count(field.name))    
                else:
                    q=None
                    
                if q:
                    self.summary[field.name] = q                                    

                summarize = { 'table': self.table, 'fields': self.summary }

        return summarize
    
    def group(self):

        grouping = {}
        if self.model:
            q={}
            self.grouping = {}
            # basic grouping on char fields    
            for field in self.opts.fields:
                if isinstance(field, CharField):
                    new_aggregates = []
                    #group on choices tuple
                    if field.choices:
                        for choice in field.choices:
                            aggregates = self.model.objects.values(field.name).annotate(count=Count(field.name))
                            new_aggregates = []
                            agg = {}
                            for aggregate in aggregates:
                                new_aggregates.append({ 'count': aggregate['count'], 'label':aggregate[field.name] })
                            self.grouping[field.name] = new_aggregates

                #group on foreignkey if related table has field 'name'
                elif isinstance(field, models.ForeignKey):
                    for fld in field.related.parent_model._meta.fields:

                        if Related.objects.filter(app_label = self.app_label, model_name = self.model_name, field_name = field.name, related_to_model = field.related.parent_model._meta.module_name ):
                            related = Related.objects.get(app_label = self.app_label, model_name = self.model_name, field_name = field.name, related_to_model = field.related.parent_model._meta.module_name )
                            related_to_field_name = related.related_to_field_name
                        else:
                            related_to_field_name = 'name'  
                                                  
                        if fld.name == related_to_field_name:
                            fld_string = '%s__%s' % (field.name, fld.name)                        
                            aggregates = self.model.objects.values(fld_string).annotate(count=Count(fld_string))
                            new_aggregates = []
                            #self.grouping[fld_string] = q
                            for aggregate in aggregates:
                                new_aggregates.append({ 'count': aggregate['count'], 'label':aggregate[fld_string] })
                            self.grouping[field.name] = new_aggregates        
                            
            grouping = { 'table': self.table, 'fields': self.grouping }

        return grouping
        
        
    def group_m2m(self):
    
        for field in self.opts.local_many_to_many:
            for fld in field.related.parent_model._meta.fields:
                if Related.objects.filter(app_label = self.app_label, model_name = self.model_name, field_name = field.name, related_to_model = field.related.parent_model._meta.module_name ):
                    related = Related.objects.get(app_label = self.app_label, model_name = self.model_name, field_name = field.name, related_to_model = field.related.parent_model._meta.module_name )
                    related_to_field_name = related.related_to_field_name
                else:
                    related_to_field_name = 'name'  
                                          
                if fld.name == related_to_field_name:
                    fld_string = '%s__%s' % (field.name, fld.name)                        
                    aggregates = self.model.objects.values(fld_string).annotate(count=Count(fld_string))
                    new_aggregates = []
                    for aggregate in aggregates:
                        new_aggregates.append({ 'count': aggregate['count'], 'label':aggregate[fld_string] })
                    self.grouping_m2m[field.name] = new_aggregates        

        return { 'table': self.table, 'fields': self.grouping_m2m }


