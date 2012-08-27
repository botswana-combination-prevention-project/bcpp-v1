import copy
from django.conf import settings
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule
#from rule import Rule
from rule_group import RuleGroup


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class Controller(object):

    """ Main controller of :class:`RuleGroup` objects. """

    def __init__(self):
        self._registry = {}
        self.dashboard_rules = []

    def set_registry(self, rule_group):
        if not issubclass(rule_group, RuleGroup):
            raise AlreadyRegistered('Expected an instance of RuleGroup.')
        if not rule_group.app_label in self._registry:
            self._registry.update({rule_group.app_label: []})
        if rule_group in self._registry.get(rule_group.app_label):
            raise AlreadyRegistered('The rule {0} is already registered for module {1}'.format(rule_group.__name__, rule_group.app_label))
        self._registry.get(rule_group.app_label).append(rule_group)

    def get_registry(self, app_label=None):
        if app_label:
            if app_label in self._registry:
                return self._registry.get(app_label)
            else:
                return {}
        return self._registry

    def register(self, rule_group):
        """ Register Rule groups to the list for the module the rule groups were declared in; which is the same module as the visit model (see update)."""
        self.set_registry(rule_group)

    def update_all(self, visit_model_instance):
        """ Given a visit model instance, run all rules in each rule group for the app_label of the visit model."""
        app_label = visit_model_instance._meta.app_label
        for rule_group in self.get_registry(app_label):
            for rule in rule_group.rules:
                rule.run(visit_model_instance)

#    def update(self, instance):
#        """ Run model rules for this model instance. """
#        self.target_model = {'add': [], 'delete': []}
#        if self._registry['scheduled']:
#            """ update status for scheduled entries """
#            for rule_group in self._registry['scheduled']:
#                for rule in dir(rule_group):
#                    if isinstance(getattr(rule_group, rule), Rule):
#                        getattr(rule_group, rule).run(instance, rule_group.Meta)

    def autodiscover(self):
        """ Autodiscover buckey rules from a bucket.py.

        * Copied from django sites and only very slightly modified
        * Auto-discover INSTALLED_APPS admin.py modules and fail silently when
          not present. This forces an import on them to register any admin bits they
          may want. """
        for app in settings.INSTALLED_APPS:
            mod = import_module(app)
            # Attempt to import the app's bucket module.
            try:
                before_import_registry = copy.copy(rule_groups._registry)
                import_module('%s.rule_groups' % app)
            except:
                # Reset the model registry to the state before the last import as
                # this import will have to reoccur on the next request and this
                # could raise NotRegistered and AlreadyRegistered exceptions
                # (see #8245).
                rule_groups._registry = before_import_registry

                # Decide whether to bubble up this error. If the app just
                # doesn't have an admin module, we can ignore the error
                # attempting to import it, otherwise we want it to bubble up.
                if module_has_submodule(mod, 'rule_groups'):
                    raise
# rules global
rule_groups = Controller()
