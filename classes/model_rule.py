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
        self._target_models = []
        
        # target_model should be a list. So you may send more
        # than one tuple (app_label, model) for the rule to be
        # run against
        self.target_model = kwargs.get('target_model')
        if not isinstance(self.target_model, list):
            raise TypeError('Attribute target_model must be a list')
        
        # you may pass a reference_instance. The default is None which means 
        # use the instance of model from the bucket.py class, 
        # but you may wish to reference a value that is not in the 
        # default model. 
        self.reference_model = kwargs.get('reference_model', None)
        self.reference_model_filter = kwargs.get('reference_model_filter')
        
        # name of model attribute of the visit model. will be used with
        # get model to get the current visit model instance
        # needed for the entry bucket
        self.visit_model_fieldname = kwargs.get('visit_model_fieldname')
        
        # logic tuple
        self.logic = kwargs.get('logic')
        
        # extract the predicate from the logic. Note that we will
        # need to update this later with the current instance
        self._raw_predicate = self.logic[self._RAW_PREDICATE]
        self._predicate = ''
        
        # extract the actions from the logic
        self._consequent_action = self.logic[self._CONSEQUENT_ACTION]
        self._alternative_action = self.logic[self._ALTERNATIVE_ACTION]
    
    #def __unicode__(self):
    #    return '%s %s' % (self._target_model._meta.object_name.lower(),self.logic, )
    
    def run(self, instance, app_label):
        
        self._target_models = []

        if not self._predicate:
            raise TypeError('self.predicate should be set in the child object. cannot be None, See method run() of %s.' % (self,)) 
    
        # for each target model tuple, convert the the actual mode
        # and append to the internal list of target models
        for target_model in self.target_model:
            if isinstance(target_model, tuple):
                self._target_models.append(get_model(target_model[self._APP_LABEL], target_model[self._MODEL_NAME]))
            else:
                self._target_models.append(get_model(app_label, target_model))    
        
        # TODO: add code for AdditionalEntryBucket
        
        ScheduledEntryBucket = get_model('bhp_entry', 'scheduledentrybucket')
        # run the rule for each target model in the list
        for target_model in self._target_models:
            if eval(self._predicate):
                ScheduledEntryBucket.objects.update_status( 
                    model = target_model,
                    visit_model_instance = getattr(instance, self.visit_model_fieldname),
                    action = self._consequent_action,
                    )
                RuleHistory.objects.create(rule = self, 
                                   model = target_model._meta.object_name.lower(), 
                                   predicate = self._predicate, 
                                   action = self._consequent_action)             
            else:
                ScheduledEntryBucket.objects.update_status( 
                    model = target_model,
                    visit_model_instance = getattr(instance, self.visit_model_fieldname),
                    action = self._alternative_action,
                    )
                RuleHistory.objects.create(rule = self, 
                                   model = target_model._meta.object_name.lower(), 
                                   predicate = self._predicate, 
                                   action = self._alternative_action)    

            
            
class CharModelRule(ModelRule):
    
    def run(self, instance, app_label):
        
        self.visit_model_instance = getattr(instance, self.visit_model_fieldname)
        
        # check if a model other than the default will be used
        # to get the field value for the predicate
        if self.reference_model:
            # get the model
            reference_model = get_model(self.reference_model[self._APP_LABEL], self.reference_model[self._MODEL_NAME]) 
            if self.reference_model_filter == 'registered_subject':           
                # filter on registered subject
                self._reference_model_instance = reference_model.objects.get(registered_subject=self.visit_model_instance.appointment.registered_subject)
            else:
                raise AttributeError('Unknown reference_model_filter. Got %s' % (self.reference_model_filter))    
        
        else:
            # use the default instance    
            self._reference_model_instance = instance 
        
        # build the predicate
        if isinstance(self._raw_predicate, tuple): 
            field_value = self._reference_model_instance.__dict__[self._raw_predicate[0]]
            value = self._raw_predicate[2]
            self._predicate = '\'%s\' == \'%s\'' % (field_value.lower(), value.lower())    
        else:    
            raise TypeError('First \'logic\' item must be a tuple of (field, operator, value). Got %s' % (self._raw_predicate, ))        
        
        # call super now that the predicate is built
        super(CharModelRule, self).run(instance, app_label)
        
        

