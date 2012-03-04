from django.db import models
from django.db.models.base import ModelBase
from django.db.models import ForeignKey
from bhp_entry.models import Entry
from bhp_content_type_map.models import ContentTypeMap


class BaseEntryBucketManager(models.Manager):

    def __init__(self, *args, **kwargs):
        
        self.visit_model_instance = None
        self.visit_definition = None
        self.report_datetime = None
        self.appointment = None
        self.entry = None
        
        super(BaseEntryBucketManager, self).__init__(*args, **kwargs)


    def set_content_type_map(self, **kwargs):

        self._set_scheduled_model(**kwargs)
        self._set_scheduled_model_instance(**kwargs)        

        if self.scheduled_model:
            self.content_type_map = ContentTypeMap.objects.get(app_label = self.scheduled_model._meta.app_label, 
                                                               name = self.scheduled_model._meta.verbose_name)
        elif self.scheduled_model_instance:    
            self.content_type_map = ContentTypeMap.objects.get(app_label = self.scheduled_model_instance._meta.app_label, 
                                                               name = self.scheduled_model_instance._meta.verbose_name)            
        else:
            raise AttributeError, 'To set content_type_map, EntryBucketManager.update_status requires attribute \'scheduled_model\' or \'scheduled_model_instance\'. Got neither'            

    def set_entry(self):
        
        # find occurrence for this visit_definition in the Entry model.
        # if not found, update_status() has nothing to do
        if Entry.objects.filter(visit_definition = self.visit_definition, content_type_map = self.content_type_map):
            self.entry = Entry.objects.get(visit_definition = self.visit_definition, content_type_map = self.content_type_map)        
        else:
            #raise AttributeError('Entry instance not found for visit_defintion=%s, content_type_map=%s' % (self.visit_definition,self.content_type_map))
            self.entry = None                        

    def set_appointment(self):
        
        self.appointment = self.visit_model_instance.appointment.__class__.objects.get(
                registered_subject = self.registered_subject, 
                visit_definition__code = self.visit_model_instance.appointment.visit_definition.code, 
                visit_instance = '0')        

    def set_visit_model_instance(self, **kwargs):

        """set visit model_instance object, try to get from visit_model if not from visit_model_instance in kwargs"""

        self.set_content_type_map(**kwargs)

        self.visit_model_instance = kwargs.get('visit_model_instance')
       
        if not self.visit_model_instance:

            self._set_visit_model(**kwargs)        
            self._set_visit_fk_name(**kwargs)

            if self.visit_fk_name:
                self.visit_model_instance = self.visit_model.objects.get(pk = self.scheduled_model_instance.__dict__[self.visit_fk_name])            
            else:
                raise ValueError('EntryBucketManager.update_status, if \'model_instance\' is not provided, \'visit_mode_instance\' is required. Got None')                

        self.visit_definition = self.visit_model_instance.appointment.visit_definition

        self.registered_subject = self.visit_model_instance.appointment.registered_subject

        self.set_appointment()

        self.report_datetime = self.visit_model_instance.report_datetime  
              
        self.set_entry()
                

    def is_keyed(self):

        """ confirm if model instance exists / is_keyed """

        #raise TypeError()

        model = models.get_model(
                        self.entry.content_type_map.content_type.app_label, 
                        self.entry.content_type_map.content_type.model)
        
        visit_fk_name = [fk for fk in [f for f in self.entry.content_type_map.model_class()._meta.fields if isinstance(f,ForeignKey)] if fk.rel.to._meta.module_name == self.visit_model_instance._meta.module_name]                                        
        
        if visit_fk_name:
            visit_fk_name = visit_fk_name[0].name
            if model.objects.filter(** { visit_fk_name:self.visit_model_instance }):
                is_keyed = True            
            else:
                is_keyed = False
        else:
            raise AttributeError('Attribute \'visit_fk_name\' is required for method is_keyed in %s' % (self,))             
        
        return is_keyed                

    def get_status(self, **kwargs):

        action = kwargs.get("action")
        report_datetime = kwargs.get("report_datetime")
        current_status = kwargs.get("current_status")
        entry_comment = kwargs.get("comment")


        if self.is_keyed():
            current_status = 'KEYED' 
        else:           
            current_status = 'NEW'
    
        if current_status == 'KEYED' and not action == 'delete':
            report_datetime = report_datetime
            if action == 'not_required':
                entry_comment = 'NOT REQUIRED!'
            
        else:        
            if action == 'add_change':
                report_datetime = report_datetime
                current_status = 'KEYED'
                entry_comment = ''                
            elif action == 'delete':
                report_datetime = None
                current_status = 'NEW'
                entry_comment = 'deleted'
            elif action == 'new':
                report_datetime = None
                current_status = 'NEW'
                entry_comment = 'required'
            elif action == 'not_required':
                report_datetime = None
                current_status = 'NOT_REQUIRED'
                entry_comment = ''
            else:
                raise ValueError, 'In update_status, value of \'action\' is unhandled. Got %s.' % action

        close_datetime = None                

        return {'action': action.upper(), 
                'report_datetime': report_datetime, 
                'entry_comment':entry_comment,
                'close_datetime':close_datetime,
                }


    def _set_scheduled_model(self, **kwargs):

        """ needed to determine the foreignkey that points to the visit model and content_type_map"""

        self.scheduled_model = kwargs.get('model')
        if self.scheduled_model:
            if not isinstance(self.scheduled_model, ModelBase):
                raise ValueError('EntryBucketManager.update_status, \'model\' must be type ModelBase, is this an instance? Got %s' % (self.scheduled_model,))

        
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
            if not visit_fk:            
                raise AttributeError, 'EntryBucketManager.update_status model instance \'%s\' does not have a key to the visit_model \'%s\'. Correct the model instance passed to the manager.' % (self.scheduled_model_instance._meta.module_name, self.visit_model._meta.module_name,)                                        
        else:
            raise AttributeError, 'To set visit_fk_name, EntryBucketManager.update_status requires attribute \'scheduled_model\' or \'scheduled_model_instance\'. Got neither'            

        self.visit_fk_name = '%s_id' % visit_fk[0].name     
    



        
        
        
        
        
