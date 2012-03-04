from django.db.models import get_model
from bhp_bucket.models import RuleHistory

class ModelRule(object):
    
    def __init__(self, **kwargs):
        
        """
         IF (predicate) 
         THEN 
            (consequent)
         ELSE
            (alternative)
        """
        self._APP_LABEL = 0
        self._MODEL_NAME = 1
        self._RAW_PREDICATE = 0
        self._PREDICATE = 0
        self._CONSEQUENT_ACTION = 1
        self._ALTERNATIVE_ACTION = 2
        
        self.target_model = kwargs.get('target_model')
        self.visit_model_fieldname = kwargs.get('visit_model_fieldname')
        self.logic = kwargs.get('logic')
        self._raw_predicate = self.logic[self._RAW_PREDICATE]
        self._predicate = ''
                
        self._consequent_action = self.logic[self._CONSEQUENT_ACTION]
        self._alternative_action = self.logic[self._ALTERNATIVE_ACTION]
        
        self.model = get_model(self.target_model[self._APP_LABEL], self.target_model[self._MODEL_NAME])
    
    def __unicode__(self):
        return '%s %s' % (self.model._meta.object_name.lower(),self.logic, )
    
    def run(self, instance):
        
        if not self._predicate:
            raise TypeError('self.predicate should be set in the child object. cannot be None, See method run() of %s.' % (self,)) 
    
        ScheduledEntryBucket = get_model('bhp_entry', 'scheduledentrybucket')
        
        if eval(self._predicate):
            ScheduledEntryBucket.objects.update_status( 
                model = self.model,
                visit_model_instance = getattr(instance, self.visit_model_fieldname),
                action = self._consequent_action,
                )
            RuleHistory.objects.create(rule = self, 
                               model = self.model._meta.object_name.lower(), 
                               predicate = self._predicate, 
                               action = self._consequent_action)             
        else:
            
            ScheduledEntryBucket.objects.update_status( 
                model = self.model,
                visit_model_instance = getattr(instance, self.visit_model_fieldname),
                action = self._alternative_action,
                )
            RuleHistory.objects.create(rule = self, 
                               model = self.model._meta.object_name.lower(), 
                               predicate = self._predicate, 
                               action = self._alternative_action)    

            
            
class CharModelRule(ModelRule):
    
    def run(self, instance):
        
        if isinstance(self._raw_predicate, tuple): 
            field_value = instance.__dict__[self._raw_predicate[0]]
            value = self._raw_predicate[2]
            self._predicate = '\'%s\' == \'%s\'' % (field_value.lower(), value.lower())    
        else:    
            raise TypeError('First \'logic\' item must be a tuple of (field, operator, value). Got %s' % (self._raw_predicate, ))        
        
        super(CharModelRule, self).run(instance)
        
        

