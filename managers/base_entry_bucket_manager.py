from datetime import datetime
from django.db import models
from django.db.models.base import ModelBase
from django.db.models import ForeignKey, get_model
from bhp_content_type_map.models import ContentTypeMap


class BaseEntryBucketManager(models.Manager):

    def set_content_type_map(self, **kwargs):

        self._set_scheduled_model(**kwargs)
        self._set_scheduled_model_instance(**kwargs)        

        if self.scheduled_model:
            self.content_type_map = ContentTypeMap.objects.get(app_label = self.scheduled_model._meta.app_label, name = self.scheduled_model._meta.verbose_name)
        elif self.scheduled_model_instance:    
            self.content_type_map = ContentTypeMap.objects.get(app_label = self.scheduled_model_instance._meta.app_label, name = self.scheduled_model_instance._meta.verbose_name)            
        else:
            raise AttributeError, 'To set content_type_map, EntryBucketManager.update_status requires attribute \'scheduled_model\' or \'scheduled_model_instance\'. Got neither'            

    def set_visit_model_instance(self, **kwargs):

        """set visit model_instance object, try to get from visit_model if not from visit_model_instance in kwargs"""

        self.visit_model_instance = kwargs.get('visit_model_instance')
       
        if not self.visit_model_instance:

            self._set_visit_model(**kwargs)        
            self._set_visit_fk_name(**kwargs)

            if self.visit_fk_name:
                self.visit_model_instance = self.visit_model.objects.get(pk = self.scheduled_model_instance.__dict__[self.visit_fk_name])            
            else:
                raise ValueError('EntryBucketManager.update_status, if \'model_instance\' is not provided, \'visit_mode_instance\' is required. Got None')                

    def get_status(self, **kwargs):

        action = kwargs.get("action")
        report_datetime = kwargs.get("report_datetime")
        entry_comment = kwargs.get("comment")
        
        if action == 'add_change':
            report_datetime = report_datetime
            entry_status = 'KEYED'
            entry_comment = ''                
        elif action == 'delete':
            report_datetime = None
            entry_status = 'NEW'
            entry_comment = 'deleted'
        elif action == 'new':
            report_datetime = None
            entry_status = 'NEW'
            entry_comment = 'required'
        elif action == 'not_required':
            report_datetime = None
            entry_status = 'NOT_REQUIRED'
            entry_comment = ''
        else:
            raise ValueError, 'In update_status, value of \'action\' is unhandled. Got %s.' % action
            if entry_status == 'MISSED' or entry_status == 'NEW' or entry_status == 'PENDING' or entry_status == 'NOT_REQUIRED':
                report_datetime = None
                entry_status = 'NOT_REQUIRED'
                entry_comment = comment
            else:
                raise TypeError("EntryBucketManager cannot change value of attribute entry_status to 'not required'")

        close_datetime = None                

        return {'action': action, 
                'report_datetime': report_datetime, 
                'entry_status': entry_status, 
                'entry_comment':entry_comment,
                'close_datetime':close_datetime,
                }


    def _set_scheduled_model(self, **kwargs):

        """ needed to determine the foreignkey that points to the visit model and content_type_map"""

        self.scheduled_model = kwargs.get('model')
        if self.scheduled_model:
            if not isinstance(self.scheduled_model, ModelBase):
                raise ValueError('EntryBucketManager.update_status, \'model\' must be type ModelBase, is this an instance?' )

        
    def _set_scheduled_model_instance(self, **kwargs):

        """ needed to determine the foreignkey that points to the visit model and content_type_map"""

        self.scheduled_model_instance = kwargs.get('model_instance')
        if self.scheduled_model_instance:
            try:
                getattr(self.scheduled_model_instance, '_meta')    
            except:    
                raise ValueError('EntryBucketManager.update_status, \'model_instance\' must be an instance of a model, not a Model.' )

    
    def _set_visit_model(self, **kwargs):

        """Needed to get visit_fk_name only if visit_model_instance is not provided"""

        self.visit_model = kwargs.get('visit_model')                

        if not self.visit_model and not self.visit_model_instance:
            raise AttributeError, 'EntryBucketManager.update_status requires attribute \'visit_model\' if visit_model_instance is not provided. Got None'

    def _set_visit_fk_name(self, **kwargs):

        self._set_scheduled_model(**kwargs)

        self._set_scheduled_model_instance(**kwargs)        

        if self.scheduled_model:
            visit_fk = [fk for fk in [f for f in self.scheduled_model._meta.fields if isinstance(f,ForeignKey)] if fk.rel.to._meta.module_name == self.visit_model._meta.module_name]            
        elif self.scheduled_model_instance:
            visit_fk = [fk for fk in [f for f in self.scheduled_model_instance._meta.fields if isinstance(f,ForeignKey)] if fk.rel.to._meta.module_name == self.visit_model._meta.module_name]                                
        else:
            raise AttributeError, 'To set visit_fk_name, EntryBucketManager.update_status requires attribute \'scheduled_model\' or \'scheduled_model_instance\'. Got neither'            

        self.visit_fk_name = '%s_id' % visit_fk[0].name     



        
        
        
        
        
