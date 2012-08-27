from django.db.models import get_model
from rule import Rule

"""

to the bucket.py in the app add something like this

    class MaternalVisitBucket(ModelBucket):

        reason_lost = AdditionalModelRule(
            logic = (('reason', 'equals', 'lost'),),
            target_model = ['maternaloffstudy'],
            registered_subject_model_name = 'appointment',
             )

        reason_death = AdditionalModelRule(
            logic = (('reason', 'equals', 'death',)),
            target_model = ['maternaloffstudy', 'maternaldeath'],
            registered_subject_model_name = 'appointment',
             )

        class Meta:
            app_label = 'maikalelo_maternal'

    bucket.register(MaternalVisit, MaternalVisitBucket, 'additional')

"""


class AdditionalModelRule(Rule):

    """ add an entry in AdditionalEntryBucket if logic """

    def __init__(self, **kwargs):

        super(AdditionalModelRule, self).__init__(**kwargs)
        self.registered_subject_model_name = kwargs.get('registered_subject_model_name', None)
        # extract the predicate from the logic. Note that we will
        # need to update this later with the current instance
        self.unresolved_predicate = self.logic
        #self._target_model_add=[]
        #self._target_model_delete=[]

    def run(self, instance, app_label):

        target_model_add = []
        target_model_delete = []
        ContentTypeMap = get_model('bhp_content_type_map', 'contenttypemap')
        # call super to build predicate
        super(AdditionalModelRule, self).run(instance, app_label)
        if self.registered_subject_model_name:
            self.registered_subject = getattr(instance, self.registered_subject_model_name).registered_subject
        else:
            self.registered_subject = instance.registered_subject
        # run the rule for each target model in the list
        for target_model in self._target_models:
            if ContentTypeMap.objects.filter(app_label=target_model._meta.app_label,
                                             model=target_model._meta.object_name.lower()):
                if eval(self._predicate):
                    target_model_add.append({'model': target_model, 'registered_subject': self.registered_subject})
                else:
                    target_model_delete.append({'model': target_model, 'registered_subject': self.registered_subject})
            else:
                raise ValueError('Cannot determine target model for bucket rule, %s' % (target_model,))

        return (target_model_add, target_model_delete,)
