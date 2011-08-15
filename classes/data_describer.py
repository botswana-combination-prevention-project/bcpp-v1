import csv
from datetime import datetime
from django.db.models import CharField, DateField, DateTimeField, DecimalField, IntegerField
from django.db import models
from django.db.models import get_model
from django.http import HttpResponse
from django.db.models import Avg, Max, Min, Count, StdDev, Variance
from bhp_describer.models import Related

"""
from bhp_common.classes import DataDescriber
d = DataDescriber('mochudi_household', 'householdstructuremember')
d.summarize()
d.group()
d.export_as_csv()
"""

class DataDescriber(object):

    def __init__(self, app_label, model_name):
        
        self.app_label = app_label
        self.model_name = model_name    
        self.model = get_model(self.app_label, self.model_name)
        self.table = '%s__%s' % (self.app_label, self.model_name)
        if not self.model:
            raise ValueError('Cannot get model of app_label %s and model_name %s.' % (self.app_label, self.model_name))
        self.opts = self.model._meta
        self.summary = {} 
        self.grouping={}           
    
    
    def summarize(self):        

        # basic summary
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
            
        
        
        return { 'table': self.table, 'fields': self.summary }
    
    def group(self):

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

        return { 'table': self.table, 'fields': self.grouping }
        




