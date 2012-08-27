import logging
from bhp_entry.classes import ScheduledEntry
from bhp_entry.models import ScheduledEntryBucket, Entry
from bhp_registration.models import RegisteredSubject
from bhp_visit_tracking.models import BaseVisitTracking
from rule import Rule

logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class ScheduledDataRule(Rule):

    def set_bucket_cls(self):
        self._bucket_cls = ScheduledEntryBucket

    def set_target_bucket_instance_id(self):
        """Sets the bucket_instance_id for the target models knowing that the filter
        instance is either an instance of BaseVisitTracking or RegisteredSubject.

        Might set to None if the current visit does not contain the target model, so users should check for None."""

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
            raise AttributeError('Attribute _target_bucket_instance_id cannot be None. Not enough information to search bucket class.')
        if not self._target_bucket_instance_id:
            if not self.get_target_content_type_map():
                logger.info('Target model {0} not found but referred to in rule {1}.'.format(self.get_target_model_cls()._meta.object_name, self))
            else:
                if not Entry.objects.filter(content_type_map=self.get_target_content_type_map()).exists():
                    logger.info('Warning: {0} referred to as a target model in rule {1} but is not scheduled in any visit definition.'.format(self.get_target_model_cls()._meta.object_name, self))

    def evaluate(self):
        """ Evaluate predicate and updates bucket instance status using the ScheduleEntry class

        Note that of the source model instance does not exist (has not been keyed yet) the predicate will be None."""
        predicate = self.get_predicate()
        if predicate:
            if eval(predicate):
                action = self.get_consequent_action()
            else:
                action = self.get_alternative_action()
            if self.get_target_bucket_instance_id():  # make sure this visit has this target model
                #print 'passing to scheduledentry for target {0}.'.format(self.get_target_model_cls())
                scheduled_entry = ScheduledEntry()
                scheduled_entry.update_status_from_rule(
                    action,
                    self.get_target_model_cls(),
                    self.get_target_bucket_instance_id(),
                    self.get_visit_model_instance(),
                    self.get_filter_instance(),  # visit_model_instance or registered subject instance
                    self.get_filter_fieldname())  # visit_model fieldname or 'registered subject'
