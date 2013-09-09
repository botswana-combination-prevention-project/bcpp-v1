from django.db.models import get_model
#from bhp_entry.classes import ScheduledEntry
from controller import rule_groups


class DashboardRule(object):

    def __init__(self, bucket_type, model, visit_model_instance, required):

        self.bucket_type = bucket_type
        if isinstance(model, tuple):
            self.model = get_model(model[0], model[1])
        else:
            self.model = model
        self.visit_model_instance = visit_model_instance
        self.required = required

    def __unicode__(self):
        return "%s %s" % (self.bucket_type, self.model)

    def run(self, **kwargs):
        pass
#        if self.bucket_type == 'scheduled':
#            self.bucket_model = get_model('bhp_entry', 'scheduledentrybucket')
#        elif self.bucket_type == 'additional':
#            # TODO: test rule.run for additional entry bucket
#            self.bucket_model = get_model('bhp_entry', 'additionalentrybucket')
#        else:
#            raise AttributeError('Invalid bucket type. Must be \'scheduled\', \'additional\'. Got %s ' % (self.bucket_type,))
#        if not self.visit_model_instance:
#            self.visit_model_instance = kwargs.get('visit_model_instance')
#        scheduled_entry = ScheduledEntry()
#        if self.required:
#            scheduled_entry.update_status(self.model, self.visit_model_instance, 'new')
#        else:
#            scheduled_entry.update_status(self.model, self.visit_model_instance, 'not_required')


class DashboardRuleContainer(object):

    def __init__(self):
        self.dashboard_rules = []
        self.index = 0

    def register(self, dashboard_rule):

        # register a rule as long as it is not already in the list
        if not dashboard_rule.__dict__ in [dashboard.__dict__ for dashboard in self.dashboard_rules]:
            self.dashboard_rules.append(dashboard_rule)

    def unregister(self, dashboard_rule):
        try:
            del self.dashboard_rules[self.dashboard_rules.index(dashboard_rule)]
        except:
            pass

    def __iter__(self):
        return iter(self.dashboard_rules)

    def __next__(self):
        while self.index < len(self.dashboard_rules):
            yield self.dashboard_rules[self.index]
            self.index += 1

    def count(self):
        return len(self.dashboard_rules)

rule_groups.dashboard_rules = DashboardRuleContainer()
