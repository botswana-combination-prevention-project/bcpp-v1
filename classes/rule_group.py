import copy
from django.db.models import get_model, Model
from django.utils.encoding import smart_str

from base_rule import BaseRule


class BaseRuleGroup(type):

    def __new__(cls, name, bases, attrs):
        """Add the Meta attributes to each rule if rule attr does not exist."""
        rules = []
        parents = [b for b in bases if isinstance(b, BaseRuleGroup)]
        if not parents:
            # If this isn't a subclass of ModelBucketBase, don't do anything special.
            return super(BaseRuleGroup, cls).__new__(cls, name, bases, attrs)
        meta = attrs.pop('Meta', None)
        for rule_name, rule in attrs.items():
            if not rule_name.startswith('__'):
                if isinstance(rule, BaseRule):
                    setattr(rule, 'name', rule_name)
                    setattr(rule, 'rule_group_name', name)
                    if meta:
                        if 'app_label' not in dir(rule):
                            setattr(rule, 'app_label', meta.app_label)
                            # check target model list and convert to classes using meta.app_label
                            target_model_list = copy.copy(rule._target_model_list)
                            for item in rule._target_model_list:
                                if isinstance(item, basestring):
                                    model_name = target_model_list.pop(target_model_list.index(item))
                                    model_cls = get_model(meta.app_label, model_name)
                                    if not model_cls:
                                        raise AttributeError('Attribute \'target_model\' in rule \'{0}.{1}\' contains a model_name that does not exist. app_label=\'{2}\', model_name=\'{3}\'.'.format(name, rule_name, meta.app_label, model_name))
                                    target_model_list.append(model_cls)
                            rule._target_model_list = target_model_list
                        if 'source_model' in dir(rule) and 'source_model' in dir(meta):
                            raise AttributeError('Cannot declare attribute \'source model\' in both a rule and class Meta for rule {0}.'.format(rule_name))
                        if not 'source_model' in dir(rule) and not 'source_model' in dir(meta):
                            raise AttributeError('Attribute \'source model\' must be declared in either the rule or class Meta (source_model=<ModelClass>) for rule {0}.'.format(rule_name))
                        if not 'source_model' in dir(rule):
                            if 'source_model' in dir(meta):
                                rule.set_source_model_cls(meta.source_model)
                        if 'filter_model' not in dir(rule):
                            if 'filter_model' in dir(meta):
                                if not isinstance(meta.filter_model, tuple):
                                    raise AttributeError('Rule Meta Attribute \'filter_model\' must be a tuple of (ModelClass, fieldname).')
                                if not issubclass(meta.filter_model[0], Model) and not isinstance(meta.filter_model[0], tuple):
                                    raise AttributeError('Rule Meta Attribute \'filter_model\' must be a tuple of (ModelClass, fieldname) or ((app_label, model_name), fieldname).')
                                rule.set_filter_model_cls(meta.filter_model[0])
                                rule.set_filter_fieldname(meta.filter_model[1])
                    rules.append(rule)
                    attrs.update({rule_name: rule})
        attrs.update({'rules': tuple(rules)})
        attrs.update({'app_label': attrs.get('__module__').split('.')[0]})
        return super(BaseRuleGroup, cls).__new__(cls, name, bases, attrs)


class RuleGroup(object):

    """ Container for :class:`ModelRule` for a given rule group.

    RuleGroups are contained by the Controller
    """
    __metaclass__ = BaseRuleGroup

    def __repr__(self):
        try:
            u = unicode(self)
        except (UnicodeEncodeError, UnicodeDecodeError):
            u = '[Bad Unicode data]'
        return smart_str(u'<%s: %s>' % (self.__class__.__name__, u))

    def run_all(self, visit_model_instance):
        for rule in self.rules:
            rule.run(visit_model_instance)
