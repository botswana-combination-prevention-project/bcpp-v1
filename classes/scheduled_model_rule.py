from django.db.models import get_model
from model_rule import ModelRule

"""
The order in which the classes are listed matters. If rules refer to the same
model, only the result of the last rule will matter. In the example below,
the target_model 'hivhistorycd4' is referred to in HivHistoryBucket and ObHistoryBucket.
Since ObHistoryBucket rules will run last, the result of the HivHistoryBucket
rule referring to target_model 'hivhistorycd4' will be overwritten.


to the bucket.py in the app add something like this


    class HivHistoryBucket(ModelBucket):

        has_cd4 = ScheduledModelRule(
            logic = (('has_cd4', 'equals', 'yes'), 'new', 'not_required'),
            target_model = ['hivhistorycd4'] ,
            visit_model_fieldname = 'maternal_visit',
             )

        arv = ScheduledModelRule(
            logic = ((('on_cont_arv', 'equals', 'yes'),('init_arv', 'equals', 'yes', 'or')), 'new', 'not_required'),
            target_model = ['hivhistoryarv'],
            visit_model_fieldname = 'maternal_visit',
             )

        class Meta:
            app_label = 'maikalelo_maternal'

    bucket.register(HivHistory, HivHistoryBucket)


    class ObHistoryBucket(ModelBucket):

        is_hiv_pos = ScheduledModelRule(
            reference_model = ('maikalelo_maternal','maternalenrollment',),
            reference_model_filter = 'registered_subject',
            logic = (('is_hiv_pos', 'equals', 'yes'), 'new', 'not_required'),
            target_model = ['demographichiv','deliveryhiv','hivhistory','hivhistorycd4', 'hivhistoryvl','hivhistorytest', 'hivhistoryarv'],
            visit_model_fieldname = 'maternal_visit',
             )

        class Meta:
            app_label = 'maikalelo_maternal'

    bucket.register(ObHistory, ObHistoryBucket)

"""


class ScheduledModelRule(ModelRule):

    """ Model rule applied to ScheduledEntryBucket, if (logic) then update entry. """

    def __init__(self, **kwargs):

        super(ScheduledModelRule, self).__init__(**kwargs)
        self._RAW_PREDICATE = 0
        self._CONSEQUENT_ACTION = 1
        self._ALTERNATIVE_ACTION = 2
        # extract the predicate from the logic. Note that we will
        # need to update this later with the current instance
        self.unresolved_predicate = self.logic[self._RAW_PREDICATE]
        # extract the actions from the logic
        self._consequent_action = self.logic[self._CONSEQUENT_ACTION]
        self._alternative_action = self.logic[self._ALTERNATIVE_ACTION]

    def run(self, instance, meta):
        """ Run the rule, test the logic. """
        self.visit_model_instance = getattr(instance, meta.visit_model_fieldname)
        # call super to build predicate, etc
        super(ScheduledModelRule, self).run(instance, meta)
        ScheduledEntryBucket = get_model('bhp_entry', 'scheduledentrybucket')
        ContentTypeMap = get_model('bhp_content_type_map', 'contenttypemap')
        # run the rule for each target model in the list
        for target_model in self._target_models:
            contenttypemap = ContentTypeMap.objects.get(app_label=target_model._meta.app_label,
                                                        model=target_model._meta.object_name.lower())
            if ScheduledEntryBucket.objects.values('id').filter(entry__content_type_map=contenttypemap):
                self._eval(instance, target_model, meta.visit_model_fieldname)
            else:
                raise ValueError('Cannot determine target model for bucket rule, %s' % (target_model,))

    def _eval(self, instance, target_model, visit_model_fieldname):
        """ Evaluate predicate and update status if true """
        ScheduledEntryBucket = get_model('bhp_entry', 'scheduledentrybucket')
        if eval(self._predicate):
            ScheduledEntryBucket.objects.update_status(
                model=target_model,
                visit_model_instance=getattr(instance, visit_model_fieldname),
                action=self._consequent_action)
            #RuleHistory.objects.create(rule = self,
            #                   model = target_model._meta.object_name.lower(),
            #                   predicate = self._predicate,
            #                   action = self._consequent_action)
        else:
            ScheduledEntryBucket.objects.update_status(
                model=target_model,
                visit_model_instance=getattr(instance, visit_model_fieldname),
                action=self._alternative_action)
            #RuleHistory.objects.create(rule = self,
            #                   model = target_model._meta.object_name.lower(),
            #                   predicate = self._predicate,
            #                   action = self._alternative_action)
