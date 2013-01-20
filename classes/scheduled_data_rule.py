import logging
from bhp_entry.classes import ScheduledEntry
from bhp_entry.models import ScheduledEntryBucket, Entry
from bhp_registration.models import RegisteredSubject
from bhp_visit_tracking.models import BaseVisitTracking
from base_rule import BaseRule

logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class ScheduledDataRule(BaseRule):

    def set_entry_cls(self):
        self._entry_cls = ScheduledEntry

    def set_bucket_cls(self):
        self._bucket_cls = ScheduledEntryBucket

    def get_action_list(self):
        return ['new', 'not_required']

    def set_target_bucket_instance_id(self):
        """Sets the bucket_instance_id for the target model knowing that the filter
        instance is either an instance of BaseVisitTracking or RegisteredSubject.

        Users should check if the set value is None which will be the case if the current visit
        does not contain the target model."""
        self._target_bucket_instance_id = None
        if isinstance(self.get_filter_instance(), BaseVisitTracking):
            if self.get_bucket_cls().objects.filter(
                    entry__content_type_map=self.get_target_content_type_map(),
                    registered_subject=self.get_filter_instance().appointment.registered_subject,
                    appointment=self.get_visit_model_instance().appointment).exists():
                bucket_instance_map = self.get_bucket_cls().objects.values('id').get(
                    entry__content_type_map=self.get_target_content_type_map(),
                    registered_subject=self.get_filter_instance().appointment.registered_subject,
                    appointment=self.get_visit_model_instance().appointment)
                self._target_bucket_instance_id = bucket_instance_map.get('id')
        elif isinstance(self.get_filter_instance(), RegisteredSubject):
            if self.get_bucket_cls().objects.filter(
                    entry__content_type_map=self.get_target_content_type_map(),
                    registered_subject=self.get_filter_instance(),
                    appointment=self.get_visit_model_instance().appointment).exists():
                bucket_instance_map = self.get_bucket_cls().objects.values('id').get(
                    entry__content_type_map=self.get_target_content_type_map(),
                    registered_subject=self.get_filter_instance(),
                    appointment=self.get_visit_model_instance().appointment)
                self._target_bucket_instance_id = bucket_instance_map.get('id')
        else:
            # filter instance is not None and is not an instance of anything we expect
            raise AttributeError('Attribute _target_bucket_instance_id cannot be None. Given an instance that is neither an instance '
                                 'of BaseVisitTracking nor RegisteredSubject.')
        if not self._target_bucket_instance_id:
            if not self.get_target_content_type_map():
                logger.info('Target model {0} not found but referred to in rule {1}. Is this model name correct?'.format(self.get_target_model_cls()._meta.object_name, self))
            else:
                if not Entry.objects.filter(content_type_map=self.get_target_content_type_map()).exists():
                    logger.info('Warning: {0} referred to as a target model in rule {1} but is not scheduled in any visit definition.'.format(self.get_target_model_cls()._meta.object_name, self))

    def evaluate(self):
        """ Evaluate predicate and calls ScheduleEntry class to updates bucket instance status.

        Note that if the source model instance does not exist (has not been keyed yet) the predicate will be None
        and the rule will not be evaluated."""
        logger.debug('Evaluating rule {0} targeted for {1}.'.format(self, self.get_target_model_cls()._meta.object_name))
        predicate = self.get_predicate()
        if predicate:
            if eval(predicate):
                action = self.get_consequent_action()
            else:
                action = self.get_alternative_action()
            if self.is_valid_action(action):
                if self.get_target_bucket_instance_id():  # make sure this visit has this target model
                    EntryCls = self.get_entry_cls()
                    entry = EntryCls()
                    entry.update_status_from_rule(
                        action,
                        self.get_target_model_cls(),
                        self.get_target_bucket_instance_id(),
                        self.get_visit_model_instance(),
                        self.get_filter_instance(),  # visit_model_instance or registered subject instance
                        self.get_filter_fieldname(),
                        self.get_comment())  # visit_model fieldname or 'registered subject'
