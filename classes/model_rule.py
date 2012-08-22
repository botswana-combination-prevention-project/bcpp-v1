from django.db.models import get_model
from django.core.exceptions import ImproperlyConfigured
#from bhp_bucket.models import RuleHistory


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
        self._PREDICATE = 0
        self._target_models = []
        self._reference_model_instance = None
        # target_model should be a list. So you may send more
        # than one tuple (app_label, model name) for the rule to be
        # run against, (or a list of model names as long as
        # the Meta.app_label is set)
        self.unresolved_target_models = kwargs.get('target_model')
        if not isinstance(self.unresolved_target_models, list):
            raise TypeError('Attribute target_model must be a list')
        # you may pass a reference_instance. The default is None which means
        # use the instance of model from the bucket.py class,
        # but you may wish to reference a value that is not in the
        # default model.
        self.unresolved_reference_model = kwargs.get('reference_model', None)
        self.reference_model_filter = kwargs.get('reference_model_filter')
        # name of model attribute of the visit model. will be used with
        # get model to get the current visit model instance
        # needed for the entry bucket
        #self.visit_model_fieldname = kwargs.get('visit_model_fieldname')
        if 'visit_model_fieldname' in kwargs.keys():
            raise ImproperlyConfigured('Attribute \'visit_model_fieldname\' should not be a ModelRule class attribute. Declare in Meta.')
        # logic tuple
        self.logic = kwargs.get('logic')
        if not isinstance(self.logic, tuple):
            raise TypeError('Attribute logic must be a tuple')
        self._predicate = ''
        if not 'Meta' in dir(self):
            AttributeError('class Meta with the app_label attribute has not been defined. Do so in the bucket.py')

    def run(self, instance, meta):
        """ Run the rule. """
        self._set_reference_model(instance, meta.app_label, meta.visit_model_fieldname)
        self._build_predicate(instance)
        self._set_target_model(instance, meta.app_label)
        if not self._predicate:
            raise TypeError('self._predicate should be set in the child object. cannot be None, See method run() of %s.' % (self,))
        if not self._target_models:
            raise TypeError('self._target_models should be set in the child object. cannot be None, See method run() of %s.' % (self,))

    def _set_target_model(self, instance, app_label):
        """ Set the target model for this rule. """
        self._target_models = []
        # for each target model tuple, get the actual model
        # and append to the internal list of target models to run against
        for target_model in self.unresolved_target_models:
            if isinstance(target_model, tuple):
                self._target_models.append(get_model(target_model[self._APP_LABEL], target_model[self._MODEL_NAME]))
            else:
                self._target_models.append(get_model(app_label, target_model))

    def _set_reference_model(self, instance, app_label, visit_model_fieldname):
        """ Set the reference model used to get a field value for the predicate. """
        # check if a model other than the default will be used
        # to get the field value for the predicate
        if self.unresolved_reference_model:
            # get the model
            reference_model = get_model(self.unresolved_reference_model[self._APP_LABEL], self.unresolved_reference_model[self._MODEL_NAME])
            # check if there is a key to the visit_model or registered subject
            if not self.reference_model_filter:
                for field in reference_model._meta.fields:
                    if field.attname == visit_model_fieldname:
                        self.reference_model_filter = visit_model_fieldname
                        self._reference_model_instance = reference_model.objects.get(**{visit_model_fieldname: self.visit_model_instance})
                        break
            if not self.reference_model_filter:
                for field in reference_model._meta.fields:
                    if field.attname == 'registered_subject':
                        self.reference_model_filter = 'registered_subject'
                        self._reference_model_instance = reference_model.objects.get(registered_subject=self.visit_model_instance.appointment.registered_subject)
                        break
            if not self.reference_model_filter:
                raise AttributeError('Unknown reference_model_filter. Expected {0} or registered_subject. Got {1}'.format(visit_model_fieldname, self.reference_model_filter))
            if self.reference_model_filter == 'registered_subject':
                self._reference_model_instance = reference_model.objects.get(registered_subject=self.visit_model_instance.appointment.registered_subject)
            if not self._reference_model_instance:
                raise AttributeError('Unable to get an instance of class {0}. Need a valid reference_model_filter. Got {1}.'.format(reference_model, self.reference_model_filter))
        else:
            # use the default instance
            self._reference_model_instance = instance

    def _build_predicate(self, instance):
        """ Build the predicate. """
        # the unresolved predicate is a tuple with three items (field, operator, value)
        # or a tuple of tuples where all but the first tuple have
        # a boolean operator as an additional and fourth item
        # ((field, operator, value), (field, operator, value, boolean_operator))
        self._predicate = ''
        if isinstance(self.unresolved_predicate[0], basestring):
            self.unresolved_predicate = (self.unresolved_predicate,)
        # build the predicate
        # check that unresolved predicate is a tuple
        if not isinstance(self.unresolved_predicate, tuple):
            raise TypeError('First \'logic\' item must be a tuple of (field, operator, value). Got %s' % (self.unresolved_predicate,))
        n = 0
        for item in self.unresolved_predicate:
            if n == 0 and not len(item) == 3:
                ValueError('The logic tuple (or the first tuple of tuples) must must have three items')
            if n > 0 and not len(item) == 4:
                ValueError('Additional tuples in the logic tuple must have a boolean operator as the fourth item')
            # value from reference model field
            #try:
                #field_value = self._reference_model_instance.__dict__[item[0]]
            field_value = getattr(self._reference_model_instance, item[0])
            #except:
            #    raise ValueError('Field name in tuple %s does not exist in reference model %s' % (item[0], self.unresolved_reference_model))
            # comparison value
            value = item[2]
            # boolean operator if more than one tuple in the logic tuple
            if len(item) == 4:
                boolean_operator = item[3]
                if boolean_operator not in ['and', 'or', 'and not', 'or not']:
                    ValueError('Illegal operator in logic tuple for rule %s' % (self))
            else:
                boolean_operator = ''
            # add as string for eval
            self._predicate += ' %s (\'%s\' == \'%s\')' % (boolean_operator, field_value.lower(), value.lower())
            n += 1
