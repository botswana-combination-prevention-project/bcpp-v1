from django.db.models import get_model
from bhp_entry.models import ScheduledEntryBucket

class Action(object):
    
    def __init__(self, **kwargs):
        
        """
         IF (predicate) 
         THEN 
            (consequent)
         ELSE
            (alternative)
        """
        self.APP_LABEL = 0
        self.MODEL_NAME = 1
        self.FIELD = 0
        self.PREDICATE_OPERATOR = 1
        self.PREDICATE_VALUE = 2
        self.CONSEQUENT_ACTION = 3
        self.ALTERNATIVE_ACTION = 3
        
        self.target_model = kwargs.get('target_model')
        self.visit_model_fieldname = kwargs.get('visit_model_fieldname')
        self.logic = kwargs.get('logic')
        self.field = self.logic(self.FIELD)
        if self.PREDICATE_OPERATOR == 'equals':
            self.operator = '=='
        else:
            raise TypeError('Unknown operator')
                
        self.consequent_action = self.logic(self.CONSEQUENT_ACTION)
        self.alternative_action = self.logic(self.ALTERNATIVE_ACTION)
        self.model = get_model(self.target_model(self.APP_LABEL), self.target_model(self.MODEL_NAME))

    
    def run(self, instance):
        
        field_value = instance.__dict__[self.field]
        self.predicate = '%s %s %s' % (field_value, self.operator, self.PREDICATE_VALUE)

        if eval(self.predicate):
            ScheduledEntryBucket.objects.update_status( 
                model = self.model,
                visit_model_instance = instance.__dict__[self.visit_model_fieldname],
                action = self.consequent_action,
                )
        else:
            ScheduledEntryBucket.objects.update_status( 
                model = self.model,
                visit_model_instance = instance.__dict__[self.visit_model_fieldname],
                action = self.alternative_action,
                )
    