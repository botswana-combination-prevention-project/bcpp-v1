from django.db.models import get_model, Model
from bhp_content_type_map.models import ContentTypeMap
from bhp_registration.models import RegisteredSubject
from bhp_visit_tracking.models import BaseVisitTracking
from logic import Logic


class BaseRule(object):

    def __init__(self, *args, **kwargs):

        self._target_model_list = None
        self._target_model_cls = None
        self._source_model_cls = None
        self._filter_fieldname = None
        self._filter_instance = None
        self._filter_model_cls = None
        self._source_model_instance = None
        self._bucket_cls = None
        self._target_bucket_instance_id = None
        self._target_content_type_map = None
        self._visit_model_instance = None
        self.rule_group_name = ''

        if 'logic' in kwargs:
            if isinstance(kwargs.get('logic'), Logic):
                self.logic = kwargs.get('logic')
            else:
                raise AttributeError('Attribute \'logic\' must be an instance of class Logic.')
        if 'target_model' in kwargs:
            self.set_target_model_list(kwargs.get('target_model'))
        # these attributes usually come in thru Meta, but not always...
        if 'source_model' in kwargs:
            self.set_source_model_cls(kwargs.get('source_model'))
            # set attribute for inspection by RuleGroup
            self.source_model = kwargs.get('source_model')
        if 'filter_model' in kwargs:
            self.set_filter_model_cls(kwargs.get('filter_model')[0])
            self.set_filter_fieldname(kwargs.get('filter_model')[1])
            # set attribute for inspection by RuleGroup
            self.filter_model = kwargs.get('filter_model')

    def __repr__(self):
        return '{0}.{1}'.format(self.rule_group_name, self.name)

    def reset(self, visit_model_instance=None):
        """ Resets before run()."""
        #self._predicate = None
        #self._consequent_action = None
        #self._alternative_action = None
        # set all instances to None to force a "get"
        self._source_model_instance = None
        self._target_bucket_instance_id = None
        self._target_content_type_map = None
        self.set_visit_model_instance(visit_model_instance)
        # TODO: is this correct?
        self.set_filter_instance()

    def run(self, visit_model_instance):
        """ Run the rule, test the logic. """
        # evaluate the rule for each target model in the list
        for target_model_cls in self.get_target_model_list():
            self.reset(visit_model_instance)
            self.set_target_model_cls(target_model_cls)
            #print 'Evaluating rule {0} on target {1}'.format(self, self.get_target_model_cls()._meta.object_name)
            self.evaluate()

    def evaluate(self):
        raise AttributeError('Evaluate should be overridden. Nothing to do.')

    def set_target_model_list(self, target_model_list=None):
        """ Sets up the target model list for this rule. """
        self._target_model_list = []
        # for each target model tuple, get the actual model
        # and append to the internal list of target models to run against
        for target_model in target_model_list:
            if isinstance(target_model, tuple):
                self._target_model_list.append(get_model(target_model[0], target_model[1]))
            else:
                # oh, app_label is in Meta ...
                # we'll have to convert to classes later in RuleGroup __metaclass__
                # just store the model_name as a string for now
                self._target_model_list.append(target_model)

    def get_target_model_list(self):
        if not self._target_model_list:
            self.set_target_model_list()
        return self._target_model_list

    def set_target_model_cls(self, target_model_cls=None):
        self._target_bucket_instance_id = None
        if not target_model_cls:
            raise AttributeError('Attribute _target_model_cls cannot be None.')
        if not issubclass(target_model_cls, Model):
            # could be that something went wrong when converting from model_name to model class in RuleGroup __metaclass__
            raise AttributeError('Attribute _target_model_cls must be a Model Class. Got {0}'.format(target_model_cls))
        self._target_model_cls = target_model_cls

    def get_target_model_cls(self):
        if not self._target_model_cls:
            self.set_target_model_cls()
        return self._target_model_cls

    def set_source_model_cls(self, model_cls=None):
        """Sets the user model class where the user model class has values that will determine how to set bucket status for the target models."""
        self._source_model_instance = None
        if model_cls:
            if isinstance(model_cls, tuple):
                self._source_model_cls = get_model(model_cls[0], model_cls[1])
            else:
                self._source_model_cls = model_cls
        else:
            raise AttributeError('Attribute _source_model_cls cannot be None.')

    def get_source_model_cls(self):
        if not self._source_model_cls:
            self.set_source_model_cls()
        return self._source_model_cls

    def set_visit_model_instance(self, visit_model_instance=None):
        if not isinstance(visit_model_instance, BaseVisitTracking):
            raise TypeError('Parameter \'visit_model_instance\' must be an instance of BaseVisitTracking.')
        self._visit_model_instance = visit_model_instance
        if not self._visit_model_instance:
            raise AttributeError('Attribute _visit_model_instance cannot be None')

    def get_visit_model_instance(self):
        if not self._visit_model_instance:
            self.set_visit_model_instance()
        return self._visit_model_instance

    def set_filter_fieldname(self, filter_fieldname=None):
        """Sets the filter fieldname that is used to filter on the source_model_cls if a source_model_instance is not provided."""
        self._filter_fieldname = None
        if filter_fieldname:
            self._filter_fieldname = filter_fieldname
        else:
            raise AttributeError('Attribute _filter_fieldname cannot be None')

    def get_filter_fieldname(self):
        if not self._filter_fieldname:
            self.set_filter_fieldname()
        return self._filter_fieldname

    def set_filter_model_cls(self, model_cls=None):
        self._filter_instance = None
        if model_cls:
            if isinstance(model_cls, tuple):
                self._filter_model_cls = get_model(model_cls[0], model_cls[1])
            else:
                self._filter_model_cls = model_cls
        else:
            raise AttributeError('Attribute _filter_model_cls cannot be None.')

    def get_filter_model_cls(self):
        if not self._filter_model_cls:
            self.set_filter_model_cls()
        return self._filter_model_cls

    def set_filter_instance(self):
        """Sets the instance to filter the user model, for example an instance of a visit model or registered subject."""
        self._filter_instance = None
        if self.get_visit_model_instance():
            if self.get_filter_model_cls() == RegisteredSubject:
                self._filter_instance = self.get_visit_model_instance().appointment.registered_subject
            else:
                self._filter_instance = self.get_visit_model_instance()
        if not self._filter_instance:
            raise AttributeError('Attribute _filter_instance cannot be None')

    def get_filter_instance(self):
        if not self._filter_instance:
            self.set_filter_instance()
        return self._filter_instance

    def set_source_model_instance(self, source_model_instance=None):
        """ Set the user model instance using either a given instance or by filtering on the user model class.

        Has values that will determine how to set the bucket status for the target models.

        If the source model instance does not exixt (yet), value is None"""
        self._source_model_instance = None
        if source_model_instance:
            self._source_model_instance = source_model_instance
        elif self.get_source_model_cls()._meta.object_name.lower() == 'registeredsubject':
            # special case
            self._source_model_instance = self.get_visit_model_instance().appointment.registered_subject
        else:
            if self.get_source_model_cls().objects.filter(**{self.get_filter_fieldname(): self.get_filter_instance()}).exists():
                self._source_model_instance = self.get_source_model_cls().objects.get(**{self.get_filter_fieldname(): self.get_filter_instance()})

    def get_source_model_instance(self):
        """Gets the source model instance but users should check if the return value is None."""
        if not self._source_model_instance:
            self.set_source_model_instance()
        return self._source_model_instance

    def set_bucket_cls(self):
        """Users should override"""
        if not self._bucket_cls:
            raise AttributeError('Attribute _bucket_cls cannot be None')

    def get_bucket_cls(self):
        if not self._bucket_cls:
            self.set_bucket_cls()
        return self._bucket_cls

    def set_target_bucket_instance_id(self, bucket_cls):
        """Users should override"""
        self._target_bucket_instance_id = None
        if not self._target_bucket_instance_id:
            raise AttributeError('Attribute _target_bucket_instance_id cannot be None')

    def get_target_bucket_instance_id(self):
        if not self._target_bucket_instance_id:
            self.set_target_bucket_instance_id()
        return self._target_bucket_instance_id

    def set_target_content_type_map(self):
        """Sets the content type for the target model to help locate the target's entry bucket instance."""
        self._target_content_type_map = ContentTypeMap.objects.get(
            app_label=self.get_target_model_cls()._meta.app_label,
            model=self.get_target_model_cls()._meta.object_name.lower())

    def get_target_content_type_map(self):
        if not self._target_content_type_map:
            self.set_target_content_type_map()
        return self._target_content_type_map
